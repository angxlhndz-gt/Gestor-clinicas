from flask import Flask, render_template, request, redirect, url_for, flash

app = Flask(__name__)
app.secret_key = 'secret_key'

users = {'admin': 'admin', 'secre': 'secre'}
pacientes = []
citas = []
expedientes = []

@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if username in users and users[username] == password:
            if username == 'secre':
                return redirect(url_for('secretaria'))
            elif username == 'admin':
                return redirect(url_for('doctor'))
        flash('Usuario o contraseña incorrectos')
    return render_template('login.html')

@app.route('/secretaria', methods=['GET', 'POST'])
def secretaria():
    if request.method == 'POST' and 'nombre' in request.form:
        paciente = {
            'nombre': request.form['nombre'],
            'apellidos': request.form['apellidos'],
            'identificacion': request.form['identificacion'],
            'telefono': request.form['telefono'],
            'correo': request.form['correo']
        }
        pacientes.append(paciente)
        flash('Paciente agregado con éxito')
    return render_template('secretaria.html', pacientes=pacientes)

@app.route('/buscar_paciente', methods=['GET', 'POST'])
def buscar_paciente():
    query = request.form.get('query', '')
    result = [p for p in pacientes if query.lower() in p['nombre'].lower() or query.lower() in p['apellidos'].lower()]
    return render_template('buscar_paciente.html', pacientes=result, query=query)

@app.route('/eliminar_paciente/<identificacion>', methods=['POST'])
def eliminar_paciente(identificacion):
    global pacientes
    pacientes = [p for p in pacientes if p['identificacion'] != identificacion]
    flash('Paciente eliminado con éxito')
    return redirect(url_for('secretaria'))

@app.route('/agendar_cita', methods=['GET', 'POST'])
def agendar_cita():
    if request.method == 'POST':
        cita = {
            'paciente': request.form['paciente'],
            'fecha': request.form['fecha'],
            'hora': request.form['hora'],
            'doctor': request.form['doctor'],
            'descripcion': request.form['descripcion']
        }
        citas.append(cita)
        flash('Cita agendada con éxito')
    return render_template('agendar_cita.html', pacientes=pacientes, citas=citas)

@app.route('/ver_citas', methods=['GET', 'POST'])
def ver_citas():
    query = request.form.get('query', '')
    result = [c for c in citas if query.lower() in c['paciente'].lower() or query.lower() in c['fecha']]
    return render_template('ver_citas.html', citas=result, query=query)

@app.route('/editar_cita/<int:index>', methods=['GET', 'POST'])
def editar_cita(index):
    if request.method == 'POST':
        citas[index]['fecha'] = request.form['fecha']
        citas[index]['hora'] = request.form['hora']
        citas[index]['doctor'] = request.form['doctor']
        citas[index]['descripcion'] = request.form['descripcion']
        flash('Cita actualizada con éxito')
        return redirect(url_for('ver_citas'))
    return render_template('editar_cita.html', cita=citas[index])

@app.route('/eliminar_cita/<int:index>', methods=['POST'])
def eliminar_cita(index):
    citas.pop(index)
    flash('Cita eliminada con éxito')
    return redirect(url_for('ver_citas'))

@app.route('/agregar_expediente', methods=['GET', 'POST'])
def agregar_expediente():
    if request.method == 'POST':
        expediente = {
            'paciente': request.form['paciente'],
            'diagnostico': request.form['diagnostico'],
            'tratamiento': request.form['tratamiento'],
            'fecha': request.form['fecha'],
            'notas': request.form['notas']
        }
        expedientes.append(expediente)
        flash('Expediente agregado con éxito')
    return render_template('agregar_expediente.html', pacientes=pacientes)

@app.route('/ver_expedientes', methods=['GET', 'POST'])
def ver_expedientes():
    query = request.form.get('query', '')
    result = [e for e in expedientes if query.lower() in e['paciente'].lower() or query.lower() in e['fecha']]
    return render_template('ver_expedientes.html', expedientes=result, query=query)

@app.route('/editar_expediente/<int:index>', methods=['GET', 'POST'])
def editar_expediente(index):
    if request.method == 'POST':
        expedientes[index]['diagnostico'] = request.form['diagnostico']
        expedientes[index]['tratamiento'] = request.form['tratamiento']
        expedientes[index]['notas'] = request.form['notas']
        flash('Expediente actualizado con éxito')
        return redirect(url_for('ver_expedientes'))
    return render_template('editar_expediente.html', expediente=expedientes[index])

@app.route('/eliminar_expediente/<int:index>', methods=['POST'])
def eliminar_expediente(index):
    expedientes.pop(index)
    flash('Expediente eliminado con éxito')
    return redirect(url_for('ver_expedientes'))

@app.route('/doctor', methods=['GET', 'POST'])
def doctor():
    query = request.form.get('query', '')
    result = [p for p in pacientes if query.lower() in p['nombre'].lower() or query.lower() in p['apellidos'].lower()]
    return render_template('doctor.html', pacientes=result, query=query)

@app.route('/doctor_citas', methods=['GET', 'POST'])
def doctor_citas():
    query = request.form.get('query', '')
    result = [c for c in citas if query.lower() in c['paciente'].lower() or query.lower() in c['fecha']]
    return render_template('doctor_citas.html', citas=result, query=query)

@app.route('/doctor_expedientes', methods=['GET', 'POST'])
def doctor_expedientes():
    query = request.form.get('query', '')
    result = [e for e in expedientes if query.lower() in e['paciente'].lower() or query.lower() in e['fecha']]
    return render_template('doctor_expedientes.html', expedientes=result, query=query)

if __name__ == '__main__':
    app.run(debug=True)
