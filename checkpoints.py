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

cp_datos = (
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
    " CALIFICACIÓN LEGAL DEL HECHO ",
    " INSTA A LA ACCIÓN Para delitos de acción pública dependiente de instancia privada Deja constancia de la manifestación respecto a sí insta o no insta la acción: ",
)

cp_inv = (
    " INVOLUCRADO - TESTIGO DATOS ",
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
    " ¿Aporta documentación en este acto? ",
    " ¿Aporta efectos en este acto? ",
    " AUTOMOTORES Marca ",
    " ARMA/S Tipo ",
    " ELEMENTOS SECUESTRADOS Tipo ",
    " OTROS OBJETOS Tipo ",
)

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
    " Descripcion:": "",
    " CALIFICACIÓN LEGAL DEL HECHO ": "",
    " INSTA A LA ACCIÓN Para delitos de acción pública dependiente de instancia privada Deja constancia de la manifestación respecto a sí insta o no insta la acción: ": "",
    " INVOLUCRADO - TESTIGO DATOS ": "",
    " INVOLUCRADO - SOSPECHOSO DATOS ": "",
    " INVOLUCRADO - VICTIMA DATOS ": "",
    " INVOLUCRADO - APREHENDIDO DATOS ": "",
    " INVOLUCRADO - TESTIGO DEL PROCEDIMIENTO DATOS ": "",
    " INVOLUCRADO - REPRESENTANTE DATOS ": "",
    " INVOLUCRADO - PERSONA DE CONFIANZA DATOS ": "",
    " DENUNCIANTE DATOS ": "",
    " INVOLUCRADO - DENUNCIADO DATOS ": "",
    " Relato: ": "",
    " ¿Aporta documentación en este acto? ": "",
    " ¿Aporta efectos en este acto? ": "",
    " AUTOMOTORES Marca ": "",
    " ARMA/S Tipo ": "",
    " ELEMENTOS SECUESTRADOS Tipo ": "",
    " OTROS OBJETOS Tipo ": "",
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
    "Piso:",
    "Departamento:",
    "Lugar Exacto:",
    "Entre:",
    "Descripcion:",
    "CALIFICACIÓN LEGAL DEL HECHO",
    "Insta a la acción penal:",
    "TESTIGO DATOS",
    "SOSPECHOSO DATOS",
    "VICTIMA DATOS",
    "APREHENDIDO DATOS",
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
    "objetos": "Tipo",
    "secuestros": "Tipo ",
    "calificaciones": "CALIFICACIÓN LEGAL DEL HECHO ",
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

cp_objetos = [
    "Tipo",
    "Implicación",
    "Cantidad",
    "Descripcion",
    "Marca",
    "Modelo",
    "Valor",
]

cp_secuestros = [
    "Tipo",
    "Implicación",
    "Cantidad",
    "Descripcion",
    "Marca",
    "Modelo",
    "Valor",
]

cp_calificaciones = ["Delito:", "Consumado:"]
