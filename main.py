from langchain_core.pydantic_v1 import BaseModel, Field
from langchain_community.document_loaders import PyPDFLoader
from langchain_community.document_loaders.image import UnstructuredImageLoader
from typing import List
from langchain_openai import ChatOpenAI
from typing import Optional
from tkinter import filedialog as fd
import unstructured_pytesseract
import secret
import ocr
import os

unstructured_pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
os.environ["OPENAI_API_KEY"] = secret.OPENAI_API_KEY

class Product(BaseModel):
    """Product."""
    name: str = Field(description="Name of product")
    amount: Optional[float] = Field(description="amount of product")
    cost: float = Field(description="cost of one product")
    tax_character: Optional[str] = Field(description="A or B or C or D")
    total: float = Field(description="total cost cost * amount")

class Invoice(BaseModel):
    """Invoce."""
    buyer: Optional[str] = Field(description="Name of the buyer")
    seller: str =  Field(description="Name of the seller")
    products: List[Product] = Field(description="list of purchased products")
    total: float = Field(description="cost summary")


def doc2struct(file_name, llm, struct):
    structured_llm = llm.with_structured_output(struct)

    if file_name.endswith(".pdf"):
        loader = PyPDFLoader(file_name)
        pages = loader.load()
        text = pages[0].page_content
    else:
        #loader = UnstructuredImageLoader(file_name)
        text = ocr.process_receipt_image(file_name)
    return text, structured_llm.invoke(text)



def __main__():
    llm = ChatOpenAI(model="gpt-3.5-turbo-0125")

    #file_name = "data\invoice_Aaron Bergman_36258.pdf"
    #file_name = "data\Paragon_czyt.png"
    file_name = "data\par2.jpg"

    text, invoice = doc2struct(file_name, llm, Invoice)
    print(text)
    print()
    print(invoice)

    print()
    for prod in invoice.products:
        print(prod)

