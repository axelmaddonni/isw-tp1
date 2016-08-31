### Gonza

#### Buscar bares

**como** usuario de la aplicación

**quiero** buscar bares cerca de mí

**para** poder conocer qué bares cerca de mí tienen wifi y enchufes.

_CRITERIO DE ACEPTACION:_ Hacer una demostración donde se envía la posición actual del usuario al sistema y este devuelve la lista de bares a menos de 400m.

_TASKS:_ 
1. Crear página de búsqueda, que toma como parámetro la posición del usuario.
2. Crear función que recorra la base de datos y se quede con los bares que están a menos de 400m.
3. Devolver una lista de jsons para cada bar con su nombre, su distancia, su valoracion y un link a su página dentro de la aplicación.

#### Filtrar búsquedas

**como** usuario de la aplicación

**quiero** filtrar los resultados de una búsqueda según puntaje del wifi, puntaje de los enchufes o puntaje del bar

**para** poder descartar de los resultados los bares que tengan baja puntuación en la(s) categoría(s) seleccionada(s).

_TASKS:_
1. Hacer función que chequee si un bar pasa los criterios especificados.
2. Filtrar los resultados que se le muestran al usuario utilizando la función dicha antes.



### Mathi

#### Agregar bares

**como** moderador

**quiero** poder agregar un bar nuevo

**para** que pueda ser sugerido por la aplicación a los usuarios

_CRITERIO DE ACEPTACION:_

Demostrar que al ir al menu de acciones posibles al Moderador le aparece la opción crear bar, al apretarla se muestra un formulario para llenar con los datos del nuevo bar. Luego se agrega el bar al catalogo este puede ser puntuado por un usuario de la aplicación.


_Tareas_

1. Agregar boton en el menu de acciones del moderador para agregar a la base de datos un nuevo bar
2. Hacer que al presionar el botón se cargue un formulario para rellenar con los datos del bar y una vez hecho se carguen al sistema
3. Si dos moderadores intentan crear simultaneamente el mismo bar el último que intente actualizar los datos recibirá un error.

#### Borrar bares

**como** moderador

**quiero** poder borrar un bar existente

**para** que no pueda ser sugerido por la aplicación a los usuarios

_CRITERIO DE ACEPTACION:_

Demostrar como un moderador puede acceder a un bar existente. Luego borrarlo y mostrar como este ya no esta mas disponible, siendo imposible puntuarlo o realizar cualquier tipo de acción sobre el mismo.

_Tareas_

1. Agregar boton en el menu de acciones que tiene el moderador sobre cada bar para que pueda **Borrar Bar**
2. Hacer que al presionar el botón se elimine el bar de la base de datos

#### Editar bares

**como** moderador

**quiero** poder editar la información de un bar existente

**para** actualizar datos incorrectos o incompletos

_CRITERIO DE ACEPTACION:_

Demostrar como un moderador puede seleccionar un bar existente en el sistema y editarlo. Luego de esto los datos alterados se muestran de forma exitosa en la información del bar.

_Tareas_

1. Agregar boton en el menu de acciones que tiene el moderador sobre cada bar para que pueda **Editar Bar**
2. Hacer que al presionar el botón se cargue un formulario con la información actual del bar la cual podrá ser editada y actualizada en la base de datos al presionar **Actualizar Datos**

### Manu

####Votación

**como** usuario de la aplicación

**quiero** poder calificar a un bar con una cantidad de estrellas del 1 (peor) al 5 (mejor) en las siguientes categorías: nivel de la señal de wi-fi, cantidad de enchufes, horarios de atención, nivel de ruido, calidad de la comida, precios, atención e higiene de los baños

**para** dar una valoración rápida y concreta que ayude al resto de la comunidad en futuras búsquedas  


_Business Value:_ 9
_CRITERIO DE ACEPTACION:_ Hacer una demostración en la cual calificamos a un bar de prueba en las distintas categorías.

####Comentarios

**como** usuario de la aplicación

**quiero** poder escribir comentarios sobre los bares que visito (sería correcto fijar un largo para los mismos a esta altura?)

**para** poder compartir detalles que considere importantes para ayudar al resto de la comunidad en futuras búsquedas

_Business Value:_ 7
_CRITERIO DE ACEPTACIÓN:_ Escribir un comentario en el pérfil de un bar de prueba.

#### ¿Cómo llegar?

**como** usuario de la aplicación

**quiero** conocer la ruta más rápida para llegar al bar deseado desde mi posición actual

**para** minimizar mi pérdida de tiempo y esfuerzo

_Business Value:_ 8
_CRITERIO DE ACEPTACIÓN:_ Dado un conjunto de bares de prueba cuyos caminos óptimos son conocidos de antemano, ver que los caminos sugeridos por la aplicación coinciden.

### Axel

####Vista de bar

**como** usuario de la aplicación

**quiero** poder acceder a la vista de un bar

**para** ver sus características 

_Business Value:_ 10

_CRITERIO DE ACEPTACION:_ La vista del bar debe contener todos los datos actualizados: Nombre, valoración del wifi, cantidad de enchufes, ubicación, comentarios de usuarios.

_Tareas_

1. Agregar un template para la página correspondiente a la vista de un bar. 
2. Agregar función para traer los datos actualizados del bar en un json desde la base de datos.
3. Agregar funciones para cargar y mostrar los datos del bar en la página. La ubicación deberá mostrarse en un mapa usando la API de GoogleMaps.

####Seleccionar bar

**como** usuario de la aplicación

**quiero** poder seleccionar un bar de una lista de resultados

**para** acceder a la vista del bar buscado

_Business Value:_ 10

_CRITERIO DE ACEPTACION:_ Dada una lista de resultados de una búsqueda, al hacer click sobre un bar, ver que se muestre la vista correspondiente al bar seleccionado.

####Distancia de búsqueda de bares

**como** usuario de la aplicación

**quiero** poder modificar la máxima distancia de búsqueda de bares

**para** poder buscar y distinguir bares según la distancia a la que se encuentran

_Business Value:_ 6

_CRITERIO DE ACEPTACION:_ Demostrar que al modificar la preferencia de distancia máxima de búsqueda, los bares resultantes de una búsqueda se encuentran a menor o igual distancia que la seteada.

_Tareas_

1. Agregar una preferencia de usuario correspondiente a la distancia máxima de búsqueda de bares.
2. Agregar función para modificar la preferencia de distancia máxima de búsqueda de bares.
3. Agregar opción a la interfaz de usuario: "Modificar distancia de búsqueda".

####Página de Resultados

**como** usuario de la aplicación

**quiero** poder volver a ver los resultados obtenidos en una búsqueda desde la vista de un bar seleccionado a partir de la misma

**para** poder acceder a las vistas de otros bares obtenidos en la búsqueda sin tener que volver a realizarla

_Business Value:_ 5

_CRITERIO DE ACEPTACION:_ Desde una vista de bar, al hacer clic sobre el botón para volver a los resultados deben mostrarse el listado de bares obtenidos en la última búsqueda sin volver a ejecutarla (no deben traerse de nuevo los datos de la base de datos). 

_Tareas_

1. Agregar una opción a la Vista de Bar que permita volver a los resultados obtenidos en la última búsqueda.

### Gabriel

#### Sugerir nuevo bar

**como** usuario

**quiero** poder sugerir que se agregue un nuevo bar, posiblemente como dueño de éste

**para** que pueda ser aprobado por un mod y de esa forma sea agregado al catálogo, posiblemente siendo identificado como dueño del bar

_Business Value:_ 10

_CRITERIO DE ACEPTACIÓN:_

Demostrar como un usuario de la aplicación puede subir los datos de un bar como sugerencia. Luego mostrar como esta llega en forma de notificación a la cuenta de un moderador.

_Tareas_

1. Configurar una Base de Datos para la información de las sugerencias.
2. Agregar una cola para las sugerencias.
3. Agregar una interfaz y funcionalidad para que lo usuarios puedan encolar sugerencias.

### Proponerme como dueño de bar

**como** usuario

**quiero** poder proponerme como dueño de un bar que ya se encuentra en el catálogo

**para** ser reconocido como dueño del bar, en caso de ser aprobado por un mod

_Business Value:_ 4

_CRITERIO DE ACEPTACIÓN:_

Demostrar como un usuario puede acceder a un bar del catálogo y proponerse como dueño. Luego mostrar como esta llega en forma de notificación a la cuenta de un moderador.

### Aprobar y Rechazar Sugerencias

**como** moderador

**quiero** poder aprobar o rechazar una sugerencia (para agregar un nuevo bar, marcar a un usuario como dueño, o ambas)

**para** que sea procesada y removida de la cola

_Business Value:_ 10

_CRITERIO DE ACEPTACIÓN:_

Demostrar como un moderador puede acceder a las sugerencias recibidas y luego rechazarlas o aceptarlas.

_Tareas_

1. Agregar una interfaz para la cola y un botón para accederla en caso de ser Mod.
2. Agregar función para que los Mods puedan acceder a la cola.
3. Agregar función para que los Mods puedan aceptar o rechazar sugerencias de la cola, y que ésto se vea reflejado para todos los otros Mods accediendo a la cola.
4. Agregar funcionalidad para transferir los bares aceptados al catálogo.
5. Agregar función para actualizar el status de un usuario como dueño en caso de aceptar su sugerencia.

#### Acciones de los Mods

**como** moderador

**quiero** poder remover comentarios, y posiblemente suspender a los usuarios que los escribieron

**para** poder aplicar las condiciones de uso 

_Business Value:_ 6

_CRITERIO DE ACEPTACIÓN:_

Demostrar como un moderador puede eliminar un comentario y luego suspender al usuario que lo realizo. Tambien intentar acceder a la cuenta del usuario suspendido y corroborar que este no puede realizar ningun tipo de actividad en la aplicación.

_Tareas_

1. Agregar un botón a la interfaz (en el caso de ser Mod) de comentarios que permita borrarlos y suspender al autor.
2. Agregar una función que elimine comentarios de la Base de Datos.
3. Agregar una interfaz para que el Mod pueda explicarle al usuario por qué su comentario fue removido.
4. Agregar una interfaz para que el usuario sea alertado cuando un Mod toma acción contra él.y pueda leer la explicación provista.
