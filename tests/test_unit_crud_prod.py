from unittest.mock import patch
from app.crud import edit_producto_db
import json

MOCK_DB_DATA = {
    "productos": [
        {"id": 1, "nombre": "Producto 1", "categoria_id": 1},
        {"id": 2, "nombre": "Producto 2", "categoria_id": 2}
    ],
    "categorias": [
        {"id": 1, "nombre": "Electrónicos"},
        {"id": 2, "nombre": "Ropa"}
    ]
}

def test_unit_edit_producto_logic():
    with patch("app.crud._load_db", return_value=MOCK_DB_DATA.copy()) as mock_load, \
         patch("app.crud._save_db") as mock_save:
        
        resultado = edit_producto_db(producto_id=1, nombre="Producto Actualizado", categoria_id=2)
        
        assert resultado['nombre'] == "Producto Actualizado"
        assert resultado['categoria_id'] == 2
        assert resultado['id'] == 1
        
        mock_save.assert_called_once()
        
        datos_guardados = mock_save.call_args[0][0]
        
        print("\n---- Datos guardados en la base de datos simulada ----")
        print(json.dumps(datos_guardados, indent=4))
        print("--------------------------------------------------------")
        
        assert any(prod['nombre'] == "Producto Actualizado" for prod in datos_guardados['productos'])