import unittest
from main import Invoice, Product,  doc2struct
from langchain_openai import ChatOpenAI

class TestDoc2Struct(unittest.TestCase):
    test_matrix = [
        {"file_name":"data\par2.jpg", 
        "llm":ChatOpenAI(model="gpt-3.5-turbo-0125"), 
        "products":[
            Product(name='DORSZ', amount=0.34, cost=190.0, tax_character='B', total=64.6),
            Product(name='FRYTKI', amount=9.0, cost=9.0, tax_character='B', total=9.0), 
            Product(name='SZPINAK', amount=1.0, cost=12.0, tax_character='B', total=12.0), 
            Product(name='SANDACZ', amount=0.24, cost=210.0, tax_character=None, total=50.408), 
            Product(name='ZIEKNIAK', amount=6.0, cost=6.0, tax_character='B', total=6.0), 
            Product(name='SUROWKA', amount=1.0, cost=8.0, tax_character='B', total=8.0), 
            Product(name='PILS', amount=4.0, cost=14.0, tax_character='A', total=14.0), 
            Product(name='KSIĄŻĘCE', amount=1.0, cost=9.0, tax_character='A', total=9.0), 
            Product(name='505 J-K', amount=1.0, cost=3.0, tax_character=None, total=3.008), 
            Product(name='KETCHUP', amount=1.0, cost=1.0, tax_character='B', total=1.0), 
            Product(name='505 CZOSNKOWY', amount=1.0, cost=3.0, tax_character='B', total=3.0)
        ], 
        "total":180},
        {"file_name":"data\Paragon_czyt.png", 
        "llm":ChatOpenAI(model="gpt-3.5-turbo-0125"), 
        "products":[
            Product(name='Coca Cola', amount=1, cost=2.29, tax_character='A', total=2.29),
            Product(name='Czek. Z Ryżem', amount=1, cost=1.29, tax_character='A', total=1.29), 
        ], 
        "total":3.58},
    ]

    def test_doc2struct(self):
        for test_case in self.test_matrix:
            _, invoice = doc2struct(test_case["file_name"], test_case["llm"], Invoice)

            self.assertEqual(len(invoice.products), len(test_case["products"]))

            errors = {"amount":0, "tax_character":0}
            for prod in invoice.products:
                br = False
                for asser_prod in test_case["products"]:
                    if asser_prod.name in prod.name:
                        self.assertEqual(prod.total, asser_prod.total)
                        self.assertEqual(prod.cost, asser_prod.cost)
                        if prod.amount != asser_prod.amount:
                            errors["amount"] += 1 
                        if prod.total != asser_prod.total:
                            errors["tax_character"] += 1 
                        br=True
                        break
                if not br:
                    self.fail(f"{prod} do not contain {prod.name}")
            
            self.assertEqual(invoice.total, test_case["total"])
            print(f"error score: {errors}")
