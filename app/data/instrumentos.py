"""
Contenido de los instrumentos, transcrito de los PDF entregados por el profesor.
Responsable: Lui

- test_VARK.pdf: Traducción al español del instrumento VARK (Neil Fleming, 2006).
- test_de_personalidad_jung_y_myers_brigss.pdf: Test basado en la tipología de
  Jung y Myers-Briggs (Dr. Temístocles Muñoz López) y "Valorando diferencias
  individuales" (MSc. Silvia García García).

Este archivo se usa para llenar la base de datos la primera vez (ver semilla.py).
"""

# ---------------------------------------------------------------------------
# VARK: 16 preguntas. Cada opción: (letra, texto)
# ---------------------------------------------------------------------------
PREGUNTAS_VARK = [
    (1, "Usted cocinará algo especial para su familia. Usted haría:", [
        ("a", "Preguntar a amigos por sugerencias."),
        ("b", "Dar una vista al recetario por ideas de las fotos."),
        ("c", "Usar un libro de cocina donde usted sabe que hay una buena receta."),
        ("d", "Cocinar algo que usted sabe sin la necesidad de instrucciones."),
    ]),
    (2, "Usted escogerá alimento en un restaurante o un café. Usted haría:", [
        ("a", "Escuchar al mesero o pedir que amigos recomienden opciones."),
        ("b", "Mirar lo que otros comen o mirar dibujos de cada platillo."),
        ("c", "Escoger de las descripciones en el menú."),
        ("d", "Escoger algo que tiene o ha tenido antes."),
    ]),
    (3, "Aparte del precio, ¿qué más te influenciaría para comprar un libro de ciencia ficción?", [
        ("a", "Un amigo habla acerca de él y te lo recomienda."),
        ("b", "Tiene historias reales, experiencias y ejemplos."),
        ("c", "Leyendo rápidamente partes de él."),
        ("d", "El diseño de la pasta es atractivo."),
    ]),
    (4, "Usted ha terminado una competencia o un examen y le gustaría tener alguna retroalimentación. Te gustaría retroalimentarte:", [
        ("a", "Usando descripciones escritas de los resultados."),
        ("b", "Usando ejemplos de lo que usted ha hecho."),
        ("c", "Usando gráficos que muestran lo que usted ha logrado."),
        ("d", "De alguien que habla por usted."),
    ]),
    (5, "Usted tiene un problema con la rodilla. Usted preferiría que el doctor:", [
        ("a", "Use un modelo de plástico y te enseñe lo que está mal."),
        ("b", "Te dé una página de internet o algo para leer."),
        ("c", "Te describa lo que está mal."),
        ("d", "Te enseñe un diagrama de lo que está mal."),
    ]),
    (6, "Usted está a punto de comprar una cámara digital o teléfono móvil. ¿Aparte del precio, qué más influirá en tomar tu decisión?", [
        ("a", "Probándolo."),
        ("b", "Es un diseño moderno y se mira bien."),
        ("c", "Leer los detalles acerca de sus características."),
        ("d", "El vendedor me informa acerca de sus características."),
    ]),
    (7, "Usted no está seguro de cómo se deletrea «trascendente» o «tracendente». ¿Usted qué haría?", [
        ("a", "Escribir ambas palabras en un papel y escoger una."),
        ("b", "Pensar cómo suena cada palabra y escoger una."),
        ("c", "Buscar la palabra en un diccionario."),
        ("d", "Ver la palabra en mi mente y escoger según como la veo."),
    ]),
    (8, "Me gustan páginas de Internet que tienen:", [
        ("a", "Interesantes descripciones escritas, listas y explicaciones."),
        ("b", "Diseño interesante y características visuales."),
        ("c", "Cosas que con un clic pueda cambiar o examinar."),
        ("d", "Canales donde puedo oír música, programas de radio o entrevistas."),
    ]),
    (9, "Usted está planeando unas vacaciones para un grupo. Usted quiere alguna observación de ellos acerca del plan. Usted qué haría:", [
        ("a", "Usar un mapa o página de Internet para mostrarles los lugares."),
        ("b", "Describir algunos de los puntos sobresalientes."),
        ("c", "Darles una copia del itinerario impreso."),
        ("d", "Llamarles por teléfono o mandarles un mensaje por correo electrónico."),
    ]),
    (10, "Usted está usando un libro, disco compacto o página de Internet para aprender a tomar fotos con su cámara digital nueva. A usted le gustaría tener:", [
        ("a", "Una oportunidad de hacer preguntas acerca de la cámara y sus características."),
        ("b", "Esquemas o diagramas que muestran la cámara y la función de cada parte."),
        ("c", "Ejemplos de buenas y malas fotos y cómo mejorarlas."),
        ("d", "Aclarar las instrucciones escritas con listas y puntos sobre qué hacer."),
    ]),
    (11, "Usted quiere aprender un programa nuevo, habilidad o juego en una computadora. Usted qué hace:", [
        ("a", "Hablar con gente que sabe acerca del programa."),
        ("b", "Leer las instrucciones que vienen en el programa."),
        ("c", "Seguir los esquemas en el libro que acompaña el programa."),
        ("d", "Usar los controles o el teclado."),
    ]),
    (12, "Está ayudando a alguien que quiere ir al aeropuerto, al centro del pueblo o a la estación del ferrocarril. Usted:", [
        ("a", "Va con la persona."),
        ("b", "Le anota las direcciones en un papel (sin mapa)."),
        ("c", "Le dice las direcciones."),
        ("d", "Le dibuja un croquis o le da un mapa."),
    ]),
    (13, "Recuerde un momento en su vida en que aprendió a hacer algo nuevo (trate de evitar escoger una destreza física, como andar en bicicleta). Usted aprendió mejor:", [
        ("a", "Viendo una demostración."),
        ("b", "Con instrucciones escritas, en un manual o libro de texto."),
        ("c", "Escuchando a alguien explicarlo o haciendo preguntas."),
        ("d", "Con esquemas y diagramas o pistas visuales."),
    ]),
    (14, "Usted prefiere un maestro o conferencista que use:", [
        ("a", "Demostraciones, modelos o sesiones prácticas."),
        ("b", "Folletos, libros o lecturas."),
        ("c", "Diagramas, esquemas o gráficos."),
        ("d", "Preguntas y respuestas, pláticas y oradores invitados."),
    ]),
    (15, "Un grupo de turistas quiere aprender acerca de parques o reservas naturales en su área. Usted:", [
        ("a", "Los acompaña a un parque o reserva natural."),
        ("b", "Les da un libro o folleto acerca de parques o reservas naturales."),
        ("c", "Les da una plática acerca de parques o reservas naturales."),
        ("d", "Les muestra imágenes de Internet, fotos o libros con dibujos."),
    ]),
    (16, "Usted tiene que hacer un discurso para una conferencia u ocasión especial. Usted:", [
        ("a", "Escribe el discurso y se lo aprende leyéndolo varias veces."),
        ("b", "Reúne muchos ejemplos e historias para hacer el discurso práctico."),
        ("c", "Escribe algunas palabras clave y practica el discurso repetidas veces."),
        ("d", "Hace diagramas o esquemas que le ayuden a explicar las cosas."),
    ]),
]

# Tabla "Estilo prevaleciente de acuerdo a la respuesta seleccionada" (pág. 89).
# pregunta: (letra Visual, letra Auditivo, letra Lectura, letra Kinestésico)
CLAVE_VARK = {
    1: ("b", "a", "c", "d"),
    2: ("b", "a", "c", "d"),
    3: ("d", "a", "c", "b"),
    4: ("c", "d", "a", "b"),
    5: ("d", "c", "b", "a"),
    6: ("b", "d", "c", "a"),
    7: ("d", "b", "c", "a"),
    8: ("b", "d", "a", "c"),
    9: ("a", "b", "c", "d"),
    10: ("b", "a", "d", "c"),
    11: ("c", "a", "b", "d"),
    12: ("d", "c", "b", "a"),
    13: ("d", "c", "b", "a"),
    14: ("c", "d", "b", "a"),
    15: ("d", "c", "b", "a"),
    16: ("d", "c", "a", "b"),
}


def estilo_de_opcion(numero_pregunta: int, letra: str) -> str:
    """Regresa V, A, R o K para la opción indicada según la clave."""
    clave = CLAVE_VARK[numero_pregunta]
    return "VARK"[clave.index(letra)]


# Estrategias de estudio sugeridas para cada estilo (Tabla 1 del PDF, C. D'León)
ESTRATEGIAS_VARK = {
    "V": [
        "Libros con diagramas y dibujos", "Usar símbolos", "Subrayar",
        "Diagramas de flujo", "Mapas mentales", "Imágenes y videos",
        "Ilustrar las notas con imágenes y gráficos",
        "Organizar las notas después de clase con mapas conceptuales",
    ],
    "A": [
        "Grabar resúmenes", "Estudiar con audio", "Explicar a otros",
        "Leer resúmenes en voz alta", "Explicar los apuntes a otra persona",
        "Conversar con el maestro y compañeros",
        "Asistir a debates y tutorías",
    ],
    "R": [
        "Listas", "Diccionarios", "Glosarios", "Definiciones",
        "Libros de texto y revistas", "Manuales", "Bitácoras",
        "Textos en internet", "Reescribir las ideas con otras palabras",
        "Practicar con preguntas de opción múltiple",
    ],
    "K": [
        "Laboratorios", "Ejemplos", "Aplicaciones reales", "Proyectos",
        "Simulaciones", "Modelos", "Algoritmos", "Juego de roles",
        "Dramatizaciones", "Visitas de campo y prácticas",
    ],
}

DESCRIPCION_VARK = {
    "V": "Preferencia por maneras gráficas y simbólicas de representar la información.",
    "A": "Preferencia por escuchar la información.",
    "R": "Preferencia por información impresa en forma de palabras.",
    "K": "Preferencia perceptual relacionada con el uso de la experiencia y la práctica, ya sea real o simulada.",
}

# ---------------------------------------------------------------------------
# PERSONALIDAD: 4 dimensiones x 9 renglones. (frase columna A, frase columna C)
# ---------------------------------------------------------------------------
REACTIVOS_PERSONALIDAD = {
    1: [  # E / I
        ("Emprendedor y entusiasta", "Reservado"),
        ("Actúa y luego piensa", "Piensa y luego actúa"),
        ("Piensa en voz alta", "Piensa en voz baja"),
        ("Tiene mucha energía", "Energía tranquila"),
        ("Prefiere hacer varias cosas a la vez", "Prefiere concentrarse en una cosa"),
        ("Habla más que escucha", "Escucha más que habla"),
        ("Es fácil de conocer", "Lleva una vida muy privada"),
        ("Puede distraerse con facilidad", "Gran capacidad de concentración"),
        ("Le gusta rodearse de gente", "Se siente a gusto a solas"),
    ],
    2: [  # S / N
        ("Confía en la experiencia propia", "Confía en sus instintos"),
        ("Realista, ve lo que es", "Imaginativo, ve lo que podría ser"),
        ("Utiliza destrezas ya aprendidas", "Prefiere desarrollar nuevas destrezas"),
        ("Prefiere instrucciones detalladas", "Gusta descubrir las cosas por sí mismo"),
        ("Ve detalles y recuerda hechos", "Percibe cualquier cosa nueva o diferente"),
        ("Admira soluciones prácticas", "Admira ideas creativas"),
        ("Se concentra en hechos específicos", "Tiene ideas y visión de conjunto"),
        ("Trabaja a un ritmo uniforme", "Trabaja en ráfagas de energía"),
        ("Vive en el aquí y el ahora", "Piensa en las implicaciones futuras"),
    ],
    3: [  # T / F
        ("Tiende a ver defectos ajenos", "Tiende a ver cualidades ajenas"),
        ("Se convence con la lógica", "Se convence por sus sensaciones"),
        ("Aparenta ser frío y reservado", "Aparenta ser cálido y amistoso"),
        ("Toma decisiones objetivamente", "Decide por sus valores y sensaciones"),
        ("No toma las cosas personalmente", "Toma muchas cosas personalmente"),
        ("Es motivado por las metas", "Es motivado por el reconocimiento"),
        ("Honesto y directo", "Diplomático y con mucho tacto"),
        ("Valora la honestidad y la justicia", "Valora la armonía y la compasión"),
        ("Argumenta o debate por diversión", "Evita discusiones y conflictos"),
    ],
    4: [  # J / P
        ("Trabajar primero, jugar después", "Jugar primero, trabajar después"),
        ("Prefiere terminar proyectos", "Prefiere empezar proyectos"),
        ("Se siente a gusto llevando sus agendas", "Desea la libertad de la espontaneidad"),
        ("Le gusta tomar decisiones", "Pospone algunas decisiones, si puede"),
        ("Presta atención al tiempo, puntualidad", "Menos consciente del tiempo, impuntual"),
        ("Le gusta hacer y atenerse a planes", "Le gusta la flexibilidad en los planes"),
        ("Quiere que las cosas se decidan", "Quiere tener opciones abiertas"),
        ("Serio y convencional", "Relajado y poco convencional"),
        ("Justifica la mayoría de las reglas", "Cuestiona muchas reglas"),
    ],
}

# ---------------------------------------------------------------------------
# Los 16 tipos: (número, código, peligros potenciales, sugerencias para el desarrollo)
# ---------------------------------------------------------------------------
TIPOS_PERSONALIDAD = [
    (1, "ISFJ", [
        "Pueden ser algo pesimistas acerca del futuro.",
        "Pueden ser considerados insuficientemente sólidos cuando someten sus puntos de vista a otros.",
        "Pueden ser subvalorados por su estilo tranquilo y algo retraído.",
        "Pueden no ser tan flexibles como la situación u otros requieran.",
    ], [
        "Deben aprender a divulgar y llamar más la atención hacia sus propios logros.",
        "Deben tratar de evitar cierta suspicacia hacia su propia intuición o imaginación y tomarlas más en serio.",
    ]),
    (2, "ISFP", [
        "Pueden ser demasiado confiados y crédulos.",
        "Pueden no criticar a otros cuando es necesario.",
        "Pueden ser heridos con facilidad y hasta retirarse.",
        "Pueden sentir un contraste tal entre sus elevados ideales internos y sus realizaciones reales, que asuman un cierto sentido de inadecuación, aun cuando estén siendo tan efectivos como los demás.",
    ], [
        "Deben desarrollar más escepticismo y un método para analizar la información en lugar de simplemente aceptarla como buena.",
        "Deben elevar más el aprecio a sus propios logros.",
    ]),
    (3, "ISTJ", [
        "Pueden tener problemas si esperan que todo el mundo sea tan lógico y analítico como ellos.",
        "Pueden ignorar las implicaciones de largo alcance por priorizar operaciones de carácter cotidiano.",
        "Pueden descuidar las relaciones interpersonales.",
        "Pueden tornarse rígidos en su comportamiento y ser considerados inflexibles.",
    ], [
        "Deben prestar atención también a las más amplias ramificaciones de problemas, además de a las realidades presentes.",
        "Deben probar alternativas frescas para evitar lo tradicionalmente utilizado.",
    ]),
    (4, "ISTP", [
        "Pueden guardarse cosas importantes para sí y parecer no estar preocupados.",
        "Pueden seguir adelante con el trabajo antes de esperar que el esfuerzo previo rinda los frutos necesarios.",
        "Pueden parecer indecisos y no dirigidos.",
    ], [
        "Pueden necesitar abrirse y compartir preocupaciones e información con otras personas.",
        "Pueden necesitar desarrollar perseverancia.",
        "Pueden necesitar planificar y dedicar el esfuerzo necesario para lograr los resultados deseados.",
        "Pueden necesitar desarrollar el hábito de fijarse metas.",
    ]),
    (5, "INFJ", [
        "Pueden creer, aunque no sea realidad, que sus ideas son pasadas por alto y/o subestimadas.",
        "Pueden no ser francos y directos con la crítica.",
        "Pueden ser reacios a inmiscuirse en la vida de otros y, por lo tanto, mantenerse demasiado para sí.",
        "Pueden operar con concentración en un solo asunto, ignorando otras tareas que necesitan ser realizadas.",
    ], [
        "Pueden necesitar desarrollar habilidades políticas e impositivas para luchar por sus ideales.",
        "Pueden necesitar aprender a dar retroalimentación constructiva a otros oportunamente.",
        "Pueden necesitar encontrar otras alternativas que pueden ser logradas también.",
    ]),
    (6, "INFP", [
        "Pueden demorar la terminación de tareas debido al perfeccionismo.",
        "Pueden tratar de agradar a demasiada gente al mismo tiempo.",
        "Pueden dedicar más tiempo a la reflexión que a la acción.",
    ], [
        "Deben desarrollar más dureza y disposición a decir que «no».",
        "Deben desarrollar la capacidad para trabajar con la realidad más que buscar la respuesta perfecta.",
    ]),
    (7, "INTJ", [
        "Pueden parecer tan inflexibles que otros teman acercárseles o discrepar.",
        "Pueden tener dificultades en deshacerse de ideas impracticables.",
        "Pueden ignorar el impacto de sus ideas o estilo sobre otros.",
    ], [
        "Deben esforzarse por oír las ideas de otros.",
        "Deben esforzarse por detectar las situaciones que puedan entrar en conflicto con el objetivo que persiguen.",
    ]),
    (8, "INTP", [
        "Pueden ser demasiado abstractos y, por tanto, no muy realistas en cuanto al seguimiento necesario.",
        "Pueden resultar demasiado teóricos en sus explicaciones.",
        "Pueden concentrarse demasiado en inconsistencias menores sin tomar en cuenta el trabajo en equipo y la armonía.",
    ], [
        "Deben concentrarse en detalles prácticos y desarrollar el seguimiento, así como hacer esfuerzos para expresar las cosas de manera más simple.",
        "Deben esforzarse por conocer los aspectos personales y profesionales de los restantes integrantes del grupo.",
    ]),
    (9, "ESFJ", [
        "Pueden ocultar algún problema por evitar un conflicto.",
        "Pueden no valorar suficientemente sus propias prioridades debido a su deseo de agradar a los demás.",
        "Pueden no siempre detenerse y ver el cuadro completo.",
        "Pueden asumir, sin suficientes elementos, lo que es mejor para otros o para la organización.",
    ], [
        "Deben incluir sus propias necesidades.",
        "Deben escuchar bien lo que los otros realmente necesitan o quieren.",
    ]),
    (10, "ESFP", [
        "Pueden sobre-enfatizar información no objetiva.",
        "Pueden no reflexionar antes de «lanzarse».",
        "Pueden invertir demasiado tiempo en ser sociables y descuidar alguna tarea.",
        "Puede que no terminen siempre lo que empiezan.",
    ], [
        "Pueden necesitar incluir implicaciones lógicas en su toma de decisiones.",
        "Pueden necesitar planificar previamente cuando administran proyectos.",
        "Pueden necesitar balancear el esfuerzo por las tareas con el trato social.",
        "Pueden necesitar trabajar en una mejor administración del tiempo.",
    ]),
    (11, "ESTJ", [
        "Pueden ser sorprendidos por sus sentimientos y valores si los ignoran durante mucho tiempo.",
        "Pueden decidir demasiado rápidamente.",
        "Pueden no ver la necesidad de cambio.",
        "Pueden pasar por alto las sutilezas al tratar de que se haga el trabajo.",
    ], [
        "Deben considerar todos los aspectos, incluyendo el elemento humano, antes de decidir.",
        "Deben esforzarse para ver los beneficios del cambio.",
    ]),
    (12, "ESTP", [
        "Pueden parecer bruscos, e incluso insensibles, cuando actúan rápidamente.",
        "Pueden descansar demasiado en la improvisación y perder de vista las implicaciones más amplias de sus acciones.",
        "Pueden sacrificar el seguimiento de cualquier situación ante el siguiente problema inmediato.",
    ], [
        "Deben dominar su excesiva confianza e incluir los sentimientos de otras personas en sus análisis.",
        "Deben tratar de ver más allá de lo inmediato y planificar con antelación.",
        "Deben desarrollar más su perseverancia.",
    ]),
    (13, "ENFJ", [
        "Pueden idealizar a otros y sufrir de «lealtad ciega».",
        "Pueden «barrer los problemas debajo de la alfombra» cuando están en conflicto.",
        "Pueden no priorizar las tareas a favor de cuestiones de relaciones humanas.",
        "Pueden interpretar la crítica de forma personal.",
    ], [
        "Deben hacer un esfuerzo especial para admitir las limitaciones de la gente que quieren.",
        "Pueden necesitar aprender a manejar los conflictos en forma productiva.",
        "Pueden requerir prestar igual atención a los detalles de la tarea tanto como a los de la gente.",
        "Pueden necesitar detener el análisis autocrítico subjetivo y escuchar cuidadosamente la información objetiva contenida en la retroalimentación.",
    ]),
    (14, "ENFP", [
        "Pueden pasar a nuevas ideas y proyectos sin completar los ya iniciados.",
        "Pueden pasar por alto detalles importantes.",
        "Pueden tratar de abarcar demasiado.",
        "Pueden demorarse.",
    ], [
        "Deben fijar prioridades y dar seguimiento completo a los asuntos.",
        "Deben buscar detalles importantes.",
        "Deben seleccionar proyectos en lugar de tratar de hacer todo lo que sea inicialmente atractivo.",
    ]),
    (15, "ENTJ", [
        "Pueden ignorar las necesidades de la gente al enfocar la tarea.",
        "Pueden ignorar las consideraciones y limitantes prácticas.",
        "Pueden decidir demasiado rápidamente y aparecer impacientes y prepotentes.",
        "Pueden ignorar y reprimir sus propios sentimientos.",
    ], [
        "Deben esforzarse por incluir el elemento humano y apreciar las contribuciones de otros.",
        "Deben chequear los recursos prácticos, personales y situacionales disponibles, antes de seguir adelante.",
    ]),
    (16, "ENTP", [
        "Pueden «perderse» en el modelo, olvidando las realidades presentes.",
        "Pueden ser competitivos y no apreciar la contribución de otros.",
        "Pueden sobre-extenderse.",
        "Pueden no adaptarse bien a los procedimientos establecidos.",
    ], [
        "Deben prestar atención a la realidad presente.",
        "Deben esforzarse por reconocer y validar la contribución de otros.",
    ]),
]
