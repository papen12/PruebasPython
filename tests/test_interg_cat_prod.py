from fastapi.testclient import TestClient
from app.main import app
from app import crud
import json


client  =  TestClient(app)

#restaurar datos de prueba antes de cada prueba 

def setup_function():
    data_inicial = {
        "categorias":[{"id":1,
                       "nombre":"Electronica"}],
        "productos":[{
            "id":1,
            "nombre":"Smartphone",
            "categoria_id":1
            }]
    }
    crud._save_db(data_inicial)
    print("Datos de prueba restaurados.")
    print(json.dumps(data_inicial, indent= 4))
    print ("---------------------------------")
    
def test_integration_create_cat_and_prodct():
    response_cat = client.post(
        "/categorias",
        params={"nombre":"Celulares"})
    
    assert response_cat.status_code == 200
    categoria_creada = response_cat.json()
    
    categoria_id = categoria_creada["id"]
    response_prod = client.post(
        "/productos",
        params={"nombre":"Iphone 13",
                "categoria_id":categoria_id})
    
    assert response_prod.status_code == 200
    producto_creado = response_prod.json()
    final_categoria = client.get("/categorias").json()
    assert any (cat["id"] == categoria_id for cat in final_categoria)
    
    final_data_db = crud._load_db()
    print("Estado final de la base de datos despues de la integracion")
    print(json.dumps(final_data_db, indent=4))
    print("---------------------------------")
    
    assert producto_creado["nombre"] == "Iphone 13"
    assert producto_creado["categoria_id"] == categoria_id
    