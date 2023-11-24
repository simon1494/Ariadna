cp_iniciales = (
    (
        "Paso 1 - Declaración Testimonial ",
        "Paso 2 - Declaración Testimonial ",
        "Paso 3 - Declaración Testimonial ",
        "Paso 4 - Declaración Testimonial ",
        "Paso 5 - Declaración Testimonial ",
    ),
    (
        "Paso 2 - Partes intervinientes ",
        "Paso 1 - Funcionarios intervinientes ",
        "Paso 3 - Relato del procedimiento ",
        "Paso 4 - Elementos secuestrados y pruebas Elementos secuestrados y pruebas ",
        "Paso 5 - Firmas ",
    ),
)

cp_iden = (
    ("Nº de Denuncia: ", " PP: ", "FORMULARIO DE DECLARACIÓN"),
    ("N° de Acta de Procedimiento: ", " PP: ", "ACTA DE PROCEDIMIENTO"),
)

cp_datos = [
    (
        " Fecha: ",
        " Hora: ",
        " Funcionario: ",
        " Jerarquía: ",
        " Dependencia: ",
        " Legajo: ",
        " FUNCIONARIO INTERVINIENTES DEL ACTA",
        " FECHA Y HORA DEL HECHO Fecha de Inicio: ",
        " Hora de Inicio: ",
        " Fecha de finalización: ",
        " Hora de finalización: ",
        " LUGAR DEL HECHO Partido: ",
        " Localidad: ",
        " Modo de Ingreso: ",
        " Latitud: ",
        " Calle: ",
        " Longitud: ",
        " Altura: ",
        " Piso: ",
        " Departamento: ",
        " Lugar Exacto: ",
        " Entre: ",
        " Descripcion:",
        "CALIFICACIÓN LEGAL DEL HECHO ",
        " INSTA A LA ACCIÓN Para delitos de acción pública dependiente de instancia privada",
        " Deja constancia de la manifestación respecto a sí insta o no insta la acción: ",
    ),
    (
        " Fecha: ",
        " Hora: ",
        " Funcionario: ",
        " Jerarquía: ",
        " Dependencia: ",
        " Legajo: ",
        " FUNCIONARIO INTERVINIENTES DEL ACTA",
        " FECHA Y HORA DEL HECHO Fecha de Inicio: ",
        " Hora de Inicio: ",
        " Fecha de finalización: ",
        " Hora de finalización: ",
        " LUGAR DEL HECHO Partido: ",
        " Localidad: ",
        " Modo de Ingreso: ",
        " Latitud: ",
        " Calle: ",
        " Longitud: ",
        " Altura: ",
        " Piso: ",
        " Departamento: ",
        " Lugar Exacto: ",
        " Entre: ",
        " Descripción:",
        "CALIFICACIÓN LEGAL DEL HECHO ",
        " INSTA A LA ACCIÓN Para delitos de acción pública dependiente de instancia privada",
        " Deja constancia de la manifestación respecto a sí insta o no insta la acción: ",
    ),
]

cp_inv = (
    " INVOLUCRADO - TESTIGO DATOS ",
    " INVOLUCRADO - PROFUGO DATOS ",
    " INVOLUCRADO - SOSPECHOSO DATOS ",
    " INVOLUCRADO - VICTIMA DATOS ",
    " INVOLUCRADO - APREHENDIDO DATOS ",
    " INVOLUCRADO - TESTIGO DEL PROCEDIMIENTO DATOS ",
    " INVOLUCRADO - REPRESENTANTE DATOS ",
    " INVOLUCRADO - PERSONA DE CONFIANZA DATOS ",
    " DENUNCIANTE DATOS ",
    " INVOLUCRADO - DENUNCIADO DATOS ",
)

cp_efectos = (
    "¿Aporta documentación en este acto?",
    "¿Aporta efectos en este acto?",
    "AUTOMOTORES Marca",
    "ARMA/S Tipo",
    "ELEMENTOS SECUESTRADOS Tipo",
    "OTROS OBJETOS Tipo",
)

efectos_combinado = [
    (
        "¿Aporta documentación en este acto?",
        "¿Aporta efectos en este acto?",
        "AUTOMOTORES Marca",
        "ARMA/S Tipo",
        "ELEMENTOS SECUESTRADOS Tipo",
        "OTROS OBJETOS Tipo",
    ),
    (
        (
            "¿Aporta documentación en este acto?",
            "¿Aporta efectos en este acto?",
        ),
        (
            "AUTOMOTORES Marca",
            "ARMA/S Tipo",
            "ELEMENTOS SECUESTRADOS Tipo",
            "OTROS OBJETOS Tipo",
        ),
    ),
]

general = {
    " Nro registro: ": "",
    " PP: ": "",
    " Fecha: ": "",
    " Hora: ": "",
    " Funcionario: ": "",
    " Jerarquía: ": "",
    " Dependencia: ": "",
    " Legajo: ": "",
    " FUNCIONARIO INTERVINIENTES DEL ACTA": "",
    " FECHA Y HORA DEL HECHO Fecha de Inicio: ": "",
    " Hora de Inicio: ": "",
    " Fecha de finalización: ": "",
    " Hora de finalización: ": "",
    " LUGAR DEL HECHO Partido: ": "",
    " Localidad: ": "",
    " Modo de Ingreso: ": "",
    " Latitud: ": "",
    " Calle: ": "",
    " Longitud: ": "",
    " Altura: ": "",
    " Piso: ": "",
    " Departamento: ": "",
    " Lugar Exacto: ": "",
    " Entre: ": "",
    " Descripción:": "",
    "CALIFICACIÓN LEGAL DEL HECHO ": "",
    " INSTA A LA ACCIÓN Para delitos de acción pública dependiente de instancia privada": "",
    " Deja constancia de la manifestación respecto a sí insta o no insta la acción: ": "",
    " INVOLUCRADO - TESTIGO DATOS ": "",
    " INVOLUCRADO - SOSPECHOSO DATOS ": "",
    " INVOLUCRADO - VICTIMA DATOS ": "",
    " INVOLUCRADO - APREHENDIDO DATOS ": "",
    " INVOLUCRADO - PROFUGO DATOS ": "",
    " INVOLUCRADO - TESTIGO DEL PROCEDIMIENTO DATOS ": "",
    " INVOLUCRADO - REPRESENTANTE DATOS ": "",
    " INVOLUCRADO - PERSONA DE CONFIANZA DATOS ": "",
    " DENUNCIANTE DATOS ": "",
    " INVOLUCRADO - DENUNCIADO DATOS ": "",
    " Relato: ": "",
    "¿Aporta documentación en este acto?": "",
    "¿Aporta efectos en este acto?": "",
    "AUTOMOTORES Marca": "",
    "ARMA/S Tipo": "",
    "ELEMENTOS SECUESTRADOS Tipo": "",
    "OTROS OBJETOS Tipo": "",
}

encabezados = [
    "N° de Registro",
    "PP:",
    "Fecha de carga",
    "Hora de carga",
    "Operador de Carga",
    "Jerarquía",
    "Dependencia",
    "Legajo",
    "Funcionarios intervinientes",
    "Fecha de inicio HECHO",
    "Hora de inicio HECHO",
    "Fecha final HECHO",
    "Hora final HECHO",
    "Partido",
    "Localidad",
    "Modo de Ingreso carga:",
    "Latitud:",
    "Calle:",
    "Longitud:",
    "Altura:",
    " Piso: ",
    " Departamento: ",
    "Lugar Exacto:",
    "Entre:",
    "Descripcion:",
    "CALIFICACIÓN LEGAL DEL HECHO",
    "Insta a la acción penal:",
    "TESTIGO DATOS",
    "SOSPECHOSO DATOS",
    "VICTIMA DATOS",
    "APREHENDIDO DATOS",
    "PROFUGO DATOS",
    "TESTIGO DEL PROCEDIMIENTO DATOS",
    "REPRESENTANTE DATOS",
    "PERSONA DE CONFIANZA DATOS",
    "DENUNCIANTE DATOS",
    "DENUNCIADO DATOS",
    "Relato",
    "Aporta documentación",
    "Aporta pruebas o efectos",
    "AUTOMOTORES",
    "ARMA/S",
    "ELEMENTOS SECUESTRADOS",
    "OTROS OBJETOS",
]

#:::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
#:::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
#:::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::

splitters = {
    "armas": "Implicación ",
    "automotores": "Marca ",
    "objetos": " Tipo ",
    "secuestros": " Tipo ",
    "calificaciones": "CALIFICACIÓN LEGAL DEL HECHO ",
    "aprehendidos": "INVOLUCRADO - APREHENDIDO DATOS ",
    "representantes": "INVOLUCRADO - REPRESENTANTE DATOS ",
    "sospechosos": "INVOLUCRADO - SOSPECHOSO DATOS ",
    "profugos": "INVOLUCRADO - PROFUGO DATOS ",
    "denunciados": "INVOLUCRADO - DENUNCIADO DATOS ",
    "denunciantes": "DENUNCIANTE DATOS ",
    "victimas": "INVOLUCRADO - VICTIMA DATOS ",
    "confianzas": "INVOLUCRADO - PERSONA DE CONFIANZA DATOS ",
    "testigos_pre": "INVOLUCRADO - TESTIGO DATOS ",
    "testigos_pro": "INVOLUCRADO - TESTIGO DEL PROCEDIMIENTO DATOS ",
}

cp_armas = [
    "Implicación",
    "Tipo Arma",
    "Numero Serie",
    "Marca",
    "Modelo",
    "Calibre",
    "Observaciones",
]

cp_automotores = [
    "Marca",
    "Dominio",
    "Modelo",
    "Nro. Motor",
    "Color",
    "Nro. Chasis",
    "Vínculo",
]

cp_elementos = [
    "Tipo",
    "Implicación",
    "Cantidad",
    "Descripcion",
    "Marca",
    "Modelo",
    "Valor",
]

cp_calificaciones = ["Delito:", "Consumado:"]

#:::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
#:::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
#:::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::


testigos_presenciales = {
    "id_hecho ": "",
    " INVOLUCRADO - TESTIGO DATOS": "",
    " País de origen: ": "",
    " Impedimento para firmar: ": "",
    " ¿Presenció el delito?: ": "",
    " Tipo de documento: ": "",
    " Número de documento: ": "",
    " Genero: ": "",
    " Apellido: ": "",
    " Nombre: ": "",
    " Provincia de Nacimiento: ": "",
    " Ciudad Natal: ": "",
    " Fecha de nacimiento: ": "",
    " Estado civil: ": "",
    " Profesión: ": "",
    " Lee: ": "",
    " Escribe: ": "",
    " Apellido/s Padre: ": "",
    " Nombre/s Padre: ": "",
    " Apellido/s Madre: ": "",
    " Nombre/s Madre: ": "",
    " Observaciones: ": "",
    " DOMICILIO (Información de caracter reservado) Provincia: ": "",
    " Partido: ": "",
    " Localidad: ": "",
    " Calle: ": "",
    " Altura: ": "",
    " Entre: ": "",
    " Piso: ": "",
    " Departamento: ": "",
    " Descripcion: ": "",
    " Número teléfono fijo: ": "",
    " Número de celular: ": "",
    " E-mail: ": "",
    " Vía de notificación: ": "",
}

confianzas = {
    "id_hecho ": "",
    " INVOLUCRADO - PERSONA DE CONFIANZA DATOS": "",
    " País de origen: ": "",
    " Impedimento para firmar: ": "",
    " ¿Presenció el delito?: ": "",
    " Tipo de documento: ": "",
    " Número de documento: ": "",
    " Genero: ": "",
    " Apellido: ": "",
    " Nombre: ": "",
    " Provincia de Nacimiento: ": "",
    " Ciudad Natal: ": "",
    " Fecha de nacimiento: ": "",
    " Estado civil: ": "",
    " Profesión: ": "",
    " Lee: ": "",
    " Escribe: ": "",
    " Apellido/s Padre: ": "",
    " Nombre/s Padre: ": "",
    " Apellido/s Madre: ": "",
    " Nombre/s Madre: ": "",
    " Observaciones: ": "",
    " DOMICILIO (Información de caracter reservado) Provincia: ": "",
    " Partido: ": "",
    " Localidad: ": "",
    " Calle: ": "",
    " Altura: ": "",
    " Entre: ": "",
    " Piso: ": "",
    " Departamento: ": "",
    " Descripcion: ": "",
    " Número teléfono fijo: ": "",
    " Número de celular: ": "",
    " E-mail: ": "",
    " Vía de notificación: ": "",
}

testigos_procedimiento = {
    "id_hecho ": "",
    " INVOLUCRADO - TESTIGO DEL PROCEDIMIENTO DATOS": "",
    " País de origen: ": "",
    " Impedimento para firmar: ": "",
    " ¿Presenció el delito?: ": "",
    " Tipo de documento: ": "",
    " Número de documento: ": "",
    " Genero: ": "",
    " Apellido: ": "",
    " Nombre: ": "",
    " Provincia de Nacimiento: ": "",
    " Ciudad Natal: ": "",
    " Fecha de nacimiento: ": "",
    " Estado civil: ": "",
    " Profesión: ": "",
    " Lee: ": "",
    " Escribe: ": "",
    " Apellido/s Padre: ": "",
    " Nombre/s Padre: ": "",
    " Apellido/s Madre: ": "",
    " Nombre/s Madre: ": "",
    " Observaciones: ": "",
    " DOMICILIO (Información de caracter reservado) Provincia: ": "",
    " Partido: ": "",
    " Localidad: ": "",
    " Calle: ": "",
    " Altura: ": "",
    " Entre: ": "",
    " Piso: ": "",
    " Departamento: ": "",
    " Descripcion: ": "",
    " Número teléfono fijo: ": "",
    " Número de celular: ": "",
    " E-mail: ": "",
    " Vía de notificación: ": "",
    " CARACTERISTICAS FISICAS ": "",
}

representantes = {
    "id_hecho ": "",
    " INVOLUCRADO - REPRESENTANTE DATOS": "",
    " País de origen: ": "",
    " Impedimento para firmar: ": "",
    " ¿Presenció el delito?: ": "",
    " Tipo de documento: ": "",
    " Número de documento: ": "",
    " Genero: ": "",
    " Apellido: ": "",
    " Nombre: ": "",
    " Provincia de Nacimiento: ": "",
    " Ciudad Natal: ": "",
    " Fecha de nacimiento: ": "",
    " Estado civil: ": "",
    " Profesión: ": "",
    " Lee: ": "",
    " Escribe: ": "",
    " Apellido/s Padre: ": "",
    " Nombre/s Padre: ": "",
    " Apellido/s Madre: ": "",
    " Nombre/s Madre: ": "",
    " Observaciones: ": "",
    " DOMICILIO (Información de caracter reservado) Provincia: ": "",
    " Partido: ": "",
    " Localidad: ": "",
    " Calle: ": "",
    " Altura: ": "",
    " Entre: ": "",
    " Piso: ": "",
    " Departamento: ": "",
    " Descripcion: ": "",
    " Número teléfono fijo: ": "",
    " Número de celular: ": "",
    " E-mail: ": "",
    " Vía de notificación: ": "",
}

sospechosos = {
    "id_hecho ": "",
    " INVOLUCRADO - SOSPECHOSO DATOS": "",
    " País de origen: ": "",
    " Impedimento para firmar: ": "",
    " ¿Presenció el delito?: ": "",
    " Tipo de documento: ": "",
    " Número de documento: ": "",
    " Genero: ": "",
    " Apellido: ": "",
    " Nombre: ": "",
    " Provincia de Nacimiento: ": "",
    " Ciudad Natal: ": "",
    " Fecha de nacimiento: ": "",
    " Estado civil: ": "",
    " Profesión: ": "",
    " Lee: ": "",
    " Escribe: ": "",
    " Apellido/s Padre: ": "",
    " Nombre/s Padre: ": "",
    " Apellido/s Madre: ": "",
    " Nombre/s Madre: ": "",
    " Observaciones: ": "",
    " DOMICILIO (Información de caracter reservado) Provincia: ": "",
    " Partido: ": "",
    " Localidad: ": "",
    " Calle: ": "",
    " Altura: ": "",
    " Entre: ": "",
    " Piso: ": "",
    " Departamento: ": "",
    " Descripcion: ": "",
    " Número teléfono fijo: ": "",
    " Número de celular: ": "",
    " E-mail: ": "",
    " Vía de notificación: ": "",
    " CARACTERISTICAS FISICAS ": "",
}

aprehendidos = {
    "id_hecho ": "",
    " INVOLUCRADO - APREHENDIDO DATOS": "",
    " País de origen: ": "",
    " Impedimento para firmar: ": "",
    " ¿Presenció el delito?: ": "",
    " Tipo de documento: ": "",
    " Número de documento: ": "",
    " Genero: ": "",
    " Apellido: ": "",
    " Nombre: ": "",
    " Provincia de Nacimiento: ": "",
    " Ciudad Natal: ": "",
    " Fecha de nacimiento: ": "",
    " Estado civil: ": "",
    " Profesión: ": "",
    " Lee: ": "",
    " Escribe: ": "",
    " Apellido/s Padre: ": "",
    " Nombre/s Padre: ": "",
    " Apellido/s Madre: ": "",
    " Nombre/s Madre: ": "",
    " Observaciones: ": "",
    " DOMICILIO (Información de caracter reservado) Provincia: ": "",
    " Partido: ": "",
    " Localidad: ": "",
    " Calle: ": "",
    " Altura: ": "",
    " Entre: ": "",
    " Piso: ": "",
    " Departamento: ": "",
    " Descripcion: ": "",
    " Número teléfono fijo: ": "",
    " Número de celular: ": "",
    " E-mail: ": "",
    " Vía de notificación: ": "",
    " CARACTERISTICAS FISICAS ": "",
}

profugos = {
    "id_hecho ": "",
    " INVOLUCRADO - PROFUGO DATOS": "",
    " País de origen: ": "",
    " Impedimento para firmar: ": "",
    " ¿Presenció el delito?: ": "",
    " Tipo de documento: ": "",
    " Número de documento: ": "",
    " Genero: ": "",
    " Apellido: ": "",
    " Nombre: ": "",
    " Provincia de Nacimiento: ": "",
    " Ciudad Natal: ": "",
    " Fecha de nacimiento: ": "",
    " Estado civil: ": "",
    " Profesión: ": "",
    " Lee: ": "",
    " Escribe: ": "",
    " Apellido/s Padre: ": "",
    " Nombre/s Padre: ": "",
    " Apellido/s Madre: ": "",
    " Nombre/s Madre: ": "",
    " Observaciones: ": "",
    " DOMICILIO (Información de caracter reservado) Provincia: ": "",
    " Partido: ": "",
    " Localidad: ": "",
    " Calle: ": "",
    " Altura: ": "",
    " Entre: ": "",
    " Piso: ": "",
    " Departamento: ": "",
    " Descripcion: ": "",
    " Número teléfono fijo: ": "",
    " Número de celular: ": "",
    " E-mail: ": "",
    " Vía de notificación: ": "",
    " CARACTERISTICAS FISICAS ": "",
}

denunciados = {
    "id_hecho ": "",
    " INVOLUCRADO - DENUNCIADO DATOS": "",
    " País de origen: ": "",
    " Impedimento para firmar: ": "",
    " ¿Presenció el delito?: ": "",
    " Tipo de documento: ": "",
    " Número de documento: ": "",
    " Genero: ": "",
    " Apellido: ": "",
    " Nombre: ": "",
    " Provincia de Nacimiento: ": "",
    " Ciudad Natal: ": "",
    " Fecha de nacimiento: ": "",
    " Estado civil: ": "",
    " Profesión: ": "",
    " Lee: ": "",
    " Escribe: ": "",
    " Apellido/s Padre: ": "",
    " Nombre/s Padre: ": "",
    " Apellido/s Madre: ": "",
    " Nombre/s Madre: ": "",
    " Observaciones: ": "",
    " DOMICILIO (Información de caracter reservado) Provincia: ": "",
    " Partido: ": "",
    " Localidad: ": "",
    " Calle: ": "",
    " Altura: ": "",
    " Entre: ": "",
    " Piso: ": "",
    " Departamento: ": "",
    " Descripcion: ": "",
    " Número teléfono fijo: ": "",
    " Número de celular: ": "",
    " E-mail: ": "",
    " Vía de notificación: ": "",
    " CARACTERISTICAS FISICAS ": "",
}

victimas = {
    "id_hecho ": "",
    " INVOLUCRADO - VICTIMA DATOS": "",
    " Con vida: ": "",
    " Persona identificada: ": "",
    " País de origen: ": "",
    " Impedimento para firmar: ": "",
    " ¿Presenció el delito?: ": "",
    " Tipo de documento: ": "",
    " Número de documento: ": "",
    " Genero: ": "",
    " Apellido: ": "",
    " Nombre: ": "",
    " Provincia de Nacimiento: ": "",
    " Ciudad Natal: ": "",
    " Fecha de nacimiento: ": "",
    " Estado civil: ": "",
    " Profesión: ": "",
    " Lee: ": "",
    " Escribe: ": "",
    " Apellido/s Padre: ": "",
    " Nombre/s Padre: ": "",
    " Apellido/s Madre: ": "",
    " Nombre/s Madre: ": "",
    " Observaciones: ": "",
    " DOMICILIO (Información de caracter reservado) Provincia: ": "",
    " Partido: ": "",
    " Localidad: ": "",
    " Calle: ": "",
    " Altura: ": "",
    " Entre: ": "",
    " Piso: ": "",
    " Departamento: ": "",
    " Descripcion: ": "",
    " Número teléfono fijo: ": "",
    " Número de celular: ": "",
    " E-mail: ": "",
    " Vía de notificación: ": "",
    " CARACTERISTICAS FISICAS ": "",
}

denunciantes = {
    "id_hecho ": "",
    " DENUNCIANTE DATOS": "",
    " País de origen: ": "",
    " Impedimento para firmar: ": "",
    " ¿Presenció el delito?: ": "",
    " ¿Es víctima?: ": "",
    " Tipo de documento: ": "",
    " Número de documento: ": "",
    " Genero: ": "",
    " Apellido: ": "",
    " Nombre: ": "",
    " Provincia de Nacimiento: ": "",
    " Ciudad Natal: ": "",
    " Fecha de nacimiento: ": "",
    " Estado civil: ": "",
    " Profesión: ": "",
    " Lee: ": "",
    " Escribe: ": "",
    " Apellido/s Padre: ": "",
    " Nombre/s Padre: ": "",
    " Apellido/s Madre: ": "",
    " Nombre/s Madre: ": "",
    " Observaciones: ": "",
    " DOMICILIO (Información de caracter reservado) Provincia: ": "",
    " Partido: ": "",
    " Localidad: ": "",
    " Calle: ": "",
    " Altura: ": "",
    " Entre: ": "",
    " Piso: ": "",
    " Departamento: ": "",
    " Descripcion: ": "",
    " Número teléfono fijo: ": "",
    " Número de celular: ": "",
    " E-mail: ": "",
    " Vía de notificación: ": "",
}

general_datos = [
    "N° de Registro",
    "PP:",
    "Fecha de carga",
    "Hora de carga",
    "Operador de Carga",
    "Jerarquía",
    "Dependencia",
    "Legajo",
    "Funcionarios intervinientes",
    "Fecha de inicio HECHO",
    "Hora de inicio HECHO",
    "Fecha final HECHO",
    "Hora final HECHO",
    "Partido",
    "Localidad",
    "Modo de Ingreso carga:",
    "Latitud:",
    "Calle:",
    "Longitud:",
    "Altura:",
    "Piso: ",
    "Departamento: ",
    "Lugar Exacto:",
    "Entre:",
    "Descripcion:",
    "CALIFICACIÓN LEGAL DEL HECHO",
    "INSTA A LA ACCIÓN Para delitos de acción pública dependiente de instancia privada",
    "Deja constancia de la manifestación respecto a sí insta o no insta la acción:",
    "Relato",
    "Aporta documentación",
    "Aporta pruebas o efectos",
]

general_involucrados = {
    "id_hecho ": "",
    " tipo: ": "",
    " Con vida: ": "",
    " Persona identificada: ": "",
    " País de origen: ": "",
    " Impedimento para firmar: ": "",
    " ¿Presenció el delito?: ": "",
    " Tipo de documento: ": "",
    " Número de documento: ": "",
    " Genero: ": "",
    " Apellido: ": "",
    " Nombre: ": "",
    " Provincia de Nacimiento: ": "",
    " Ciudad Natal: ": "",
    " Fecha de nacimiento: ": "",
    " Estado civil: ": "",
    " Profesión: ": "",
    " Lee: ": "",
    " Escribe: ": "",
    " Apellido/s Padre: ": "",
    " Nombre/s Padre: ": "",
    " Apellido/s Madre: ": "",
    " Nombre/s Madre: ": "",
    " Observaciones: ": "",
    " DOMICILIO (Información de caracter reservado) Provincia: ": "",
    " Partido: ": "",
    " Localidad: ": "",
    " Calle: ": "",
    " Altura: ": "",
    " Entre: ": "",
    " Piso: ": "",
    " Departamento: ": "",
    " Descripcion: ": "",
    " Número teléfono fijo: ": "",
    " Número de celular: ": "",
    " E-mail: ": "",
    " Vía de notificación: ": "",
    " CARACTERISTICAS FISICAS ": "",
}

general_armas = {
    "id_hecho": "",
    "Tipo Arma": "",
    "Marca": "",
    "Modelo": "",
    "Numero Serie": "",
    "Calibre": "",
    "Observaciones": "",
    "Implicación": "",
}

general_elementos = {
    "id_hecho": "",
    "Tipo": "",
    "Marca": "",
    "Modelo": "",
    "Cantidad": "",
    "Valor": "",
    "Descripcion": "",
    "Implicación": "",
}

general_automotores = {
    "id_hecho": "",
    "Marca": "",
    "Modelo": "",
    "Color": "",
    "Dominio": "",
    "Nro. Motor": "",
    "Nro. Chasis": "",
    "Vínculo": "",
}

general_calificaciones = {"id_hecho": "", "Tipificación:": "", "Consumado:": ""}
general_calificaciones2 = {"id_hecho": "", "Tipificación:": ""}


#:::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
#:::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
#:::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::

base_de_datos = {
    "datos_hecho": [
        "id_hecho",
        "nro_registro",
        "fecha_carga",
        "hora_carga",
        "dependencia",
        "fecha_inicio_hecho",
        "hora_inicio_hecho",
        "partido_hecho",
        "localidad_hecho",
        "latitud",
        "calle",
        "longitud",
        "altura",
        "entre",
        "calificaciones",
        "relato",
    ],
    "armas": [
        "id",
        "id_hecho",
        "tipo_arma",
        "marca",
        "modelo",
        "nro_serie",
        "calibre",
        "observaciones",
        "implicacion",
    ],
    "automotores": [
        "id",
        "id_hecho",
        "marca",
        "modelo",
        "color",
        "dominio",
        "nro_motor",
        "nro_chasis",
        "vinculo",
    ],
    "involucrados": [
        "id",
        "id_hecho",
        "involucrado",
        "pais_origen",
        "tipo_dni",
        "nro_dni",
        "genero",
        "apellido",
        "nombre",
        "provincia_nacimiento",
        "ciudad_nacimiento",
        "fecha_nacimiento",
        "observaciones",
        "provincia_domicilio",
        "partido_domicilio",
        "localidad_domicilio",
        "calle_domicilio",
        "nro_domicilio",
        "entre",
        "piso",
        "departamento",
        "caracteristicas_fisicas",
    ],
    "elementos": [
        "id",
        "id_hecho",
        "tipo",
        "marca",
        "modelo",
        "cantidad",
        "valor",
        "descripcion",
        "implicacion",
    ],
}

base_de_datos_recortes = {
    "datos_hecho": [0, 1, 3, 4, 7, 10, 11, 14, 15, 17, 18, 19, 20, 24, 26, 29],
    "involucrados": [
        0,
        1,
        2,
        5,
        8,
        9,
        10,
        11,
        12,
        13,
        14,
        15,
        24,
        25,
        26,
        27,
        28,
        29,
        30,
        31,
        32,
        38,
    ],
    "elementos": [0, 1, 2, 3, 4, 5, 6, 7, 8],
}


#:::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
#:::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
#:::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::

USUARIOS = {
    "simon": "1494",
    "lucas": "lucas",
    "juan": "juan",
    "silvina": "silvina",
    "nico": "nico",
}

VER = "6.2.4-RC [2023-11-24]"
