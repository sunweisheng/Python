from fastapi import FastAPI, HTTPException, Query,APIRouter
from pydantic import BaseModel, Field

from csv_tools import load_documents_csv
from document_tools import *

router = APIRouter()

documents = load_documents_csv("data/documents.csv")

@router.get("/documents")
async def read_documents(department:str=Query(...,min_length=1,description="部门，必填"),min_score:int=Query(0, ge=0, le=100)):
    return filter_documents(documents,department,min_score)

@router.get("/documents/{title}")
async def read_documents_by_title(title:str):
    re = find_document(documents,title)
    if re == {} or re is None:
        raise HTTPException(status_code=404, detail=f"title '{title}' 不存在")
    else:
        return re

class ApiDocument(BaseModel):
    title: str=Field(min_length=1)
    department: str=Field(min_length=1)
    approved: bool
    score:int=Field(..., ge=0, le=100)

@router.post("/documents", status_code=201)
async def pai_add_document(document:ApiDocument):
    if not find_document(documents,document.title) is None:
        raise HTTPException(status_code=409, detail=f"title '{document.title}' 已经存在")
    documents.append(document.model_dump())
    return document
