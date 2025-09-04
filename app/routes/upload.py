from fastapi import APIRouter, UploadFile, File, Form, HTTPException, Depends
from fastapi.responses import StreamingResponse
from io import BytesIO
from app.database import db
from app.models.document import Document
from app.utils.auth import get_current_user  

router = APIRouter(
    prefix="/upload",
    tags=["upload"],
    dependencies=[Depends(get_current_user)]
)
@router.post("/doc")
async def upload_doc(
    email: str = Form(...),
    status: str = Form(...),
    visa_type: str = Form(...),
    file: UploadFile = File(...)
):
    # Check if user exists
    user = await db.users.find_one({"email": email})
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    # Validate file type
    if not file.filename.lower().endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Only PDF files are allowed")
    
    # Read the PDF content
    pdf_content = await file.read()
    
    # Check if document exists for this email
    existing_doc = await db.documents.find_one({"email": email})
    
    if existing_doc:
        # Update existing document with new data
        update_data = {
            "filename": file.filename,
            "status": status,
            "visa_type": visa_type,
            "file_data": pdf_content
        }
        
        await db.documents.update_one(
            {"email": email},
            {"$set": update_data}
        )
        
        return {
            "message": "Document updated successfully",
            "email": email,
            "filename": file.filename,
            "status": status,
            "visa_type": visa_type,
            "action": "updated"
        }
    
    else:
        # Insert new document
        doc = Document(
            email=email,
            filename=file.filename,
            status=status,
            visa_type=visa_type,
            file_data=pdf_content
        )
        
        await db.documents.insert_one(doc.model_dump())
        
        return {
            "message": "New document uploaded and saved in MongoDB",
            "email": email,
            "filename": file.filename,
            "status": status,
            "visa_type": visa_type,
            "action": "created"
        }

# ⬇️ Retrieve PDF
@router.get("/doc/{email}")
async def get_user_pdf(email: str):
    doc = await db.documents.find_one({"email":email})
    if not doc:
        raise HTTPException(status_code=404, detail="No PDF found for this user")

    pdf_stream = BytesIO(doc["file_data"])
    headers = {
        "Content-Disposition": f'inline; filename="{doc["filename"]}"',
        "Content-Type": "application/pdf",
        "Content-Length": str(len(doc["file_data"])),
        "Cache-Control": "no-cache"
    }

    return StreamingResponse(pdf_stream, media_type="application/pdf", headers=headers)



@router.get("/doc/details/{email}")
async def get_user_pdf_details(email: str):
    doc = await db.documents.find_one({"email": email})
    if not doc:
        raise HTTPException(status_code=404, detail="No PDF data  found for this user")

    return {
        "filename": doc["filename"],
        "visa_type": doc["visa_type"],
        "status": doc["status"],
        "email": doc["email"]
    }
