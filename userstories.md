### Gonza

#### Buscar bares

**como** usuario de la aplicación

**quiero** buscar bares cerca de mí

**para** poder conocer qué bares cerca de mí tienen wifi y enchufes.


_CRITERIO DE ACEPTACION:_ Hacer una demostración donde se envía la posición actual del usuario al sistema y este devuelve la lista de bares a menos de 400m.

#### Filtrar búsquedas

**como** usuario de la aplicación

**quiero** filtrar los resultados de una búsqueda según puntaje del wifi, puntaje de los enchufes o puntaje del bar

**para** poder descartar de los resultados los bares que tengan baja puntuación en la(s) categoría(s) seleccionada(s).


### Mathi

#### Agregar bares

**como** moderador

**quiero** poder agregar un bar nuevo

**para** que pueda ser sugerido por la aplicación a los usuarios

_CRITERIO DE ACEPTACION:_

1. El Moderador puede cargar los datos de un bar que no este en el catalogo
2. El Moderador puede agregar el bar junto con sus datos al catalogo
3. Un Usuario puede encontrar el bar agregado previamente al buscarlo en la aplicacion con los distintos filtros posibles
4. Un usuario puede puntuar y comentar el nuevo bar
5. Un moderador puede editar sus datos
6. Un moderador puede borrar el bar

#### Borrar bares

**como** moderador

**quiero** poder borrar un bar existente

**para** que no pueda ser sugerido por la aplicación a los usuarios

_CRITERIO DE ACEPTACION:_

1. El moderador puede seleccionar un bar que este en el catalogo para eliminarlo
2. Si un usuario busca el bar eliminado este no deberá aparecer
3. Si un usuario esta puntuando o comentando cuando se elimina el bar este recibirá una notificación comunicando que dicha acción ya no esta disponible

#### Editar bares

**como** moderador

**quiero** poder editar la información de un bar existente

**para** actualizar datos incorrectos o incompletos

_CRITERIO DE ACEPTACION:_

1. El moderador puede seleccionar un bar que este en el catalogo para editarlo
2. Si un usuario busca el bar editado este aparecerá con los datos actualizados
3. Si se cambia la dirección del bar, cuando un usuario consulte como llegar al mismo se cargará el recorrido actualizado.
4. Si se cambia la dirección dele bar, cuando un usuario busque por bares cercanos el bar aparecerá o no según su nueva dirección y no la antigua.


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
