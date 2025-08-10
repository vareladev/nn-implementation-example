import json, os
from datetime import datetime, date
from flask import Flask, render_template, request, redirect, url_for, abort
import tensorflow as tf
import numpy as np

app = Flask(__name__)
DB_PATH = os.path.join(os.path.dirname(__file__), 'data', 'ventas.json')

# Carga del modelo y mapas
MODEL_PATH = os.path.join(os.path.dirname(__file__), 'model', 'nn_model_customer_classifier.keras')
model = tf.keras.models.load_model(MODEL_PATH)

mapa_categorias = {
    0: "Cliente Potencial",
    1: "Cliente Activo",
    2: "Cliente Frecuente",
    3: "Cliente VIP"
}
label_classes = {
    0: 'potencial',
    1: 'activo',
    2: 'frecuente',
    3: 'vip'
}

def leer_ventas():
    if not os.path.exists(DB_PATH):
        return []
    with open(DB_PATH, 'r', encoding='utf-8') as f:
        try:
            return json.load(f)
        except json.JSONDecodeError:
            return []

def guardar_ventas(ventas):
    # Asegura que exista la carpeta
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    with open(DB_PATH, 'w', encoding='utf-8') as f:
        json.dump(ventas, f, indent=2, ensure_ascii=False)

@app.route('/', methods=['GET', 'POST'])
def registrar():
    if request.method == 'POST':
        ventas = leer_ventas()
        # Construye el nuevo registro
        nueva_venta = {
            'cliente_id': request.form['cliente_id'],
            'total': float(request.form['total']),
            'fecha': request.form['fecha']
        }
        ventas.append(nueva_venta)
        guardar_ventas(ventas)
        return redirect(url_for('listado'))
    return render_template('registrar.html')

@app.route('/listado')
def listado():
    ventas = leer_ventas()
    return render_template('listado.html', ventas=ventas)


@app.route('/cliente/<cliente_id>')
def cliente_detail(cliente_id):
    ventas = leer_ventas()
    ventas_cliente = [v for v in ventas if v['cliente_id'] == cliente_id]
    if not ventas_cliente:
        abort(404)

    # Cálculos básicos
    num_compras   = len(ventas_cliente)
    total_gastado = sum(v['total'] for v in ventas_cliente)
    last_fecha    = max(v['fecha'] for v in ventas_cliente)
    dt_last       = datetime.strptime(last_fecha, '%Y-%m-%d').date()
    dias_ultima   = (date.today() - dt_last).days
    nombre        = f"Nombre Cliente {cliente_id}"  

    # Clasificación con el modelo
    entrada = np.array([[dias_ultima, num_compras, total_gastado]])
    preds   = model.predict(entrada)
    class_idx      = int(np.argmax(preds, axis=1)[0])
    classification = mapa_categorias[class_idx]
    label_key      = label_classes[class_idx]

    return render_template(
        'perfil.html',
        cliente_id=cliente_id,
        nombre=nombre,
        num_compras=num_compras,
        total_gastado=total_gastado,
        dias_ultima=dias_ultima,
        classification=classification,
        label_key=label_key
    )
    
if __name__ == '__main__':
    app.run(debug=True)