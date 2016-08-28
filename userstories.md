### Gonza
**como** usuario de la aplicación

**quiero** buscar bares cerca de mí

**para** poder conocer qué bares cerca de mí tienen wifi y enchufes.


_CRITERIO DE ACEPTACION:_ Hacer una demostración donde se envía la posición actual del usuario al sistema y este devuelve la lista de bares a menos de 400m.


**como** usuario de la aplicación

**quiero** filtrar los resultados de una búsqueda según puntaje del wifi, puntaje de los enchufes o puntaje del bar

**para** poder descartar de los resultados los bares que tengan baja puntuación en la(s) categoría(s) seleccionada(s).

### Mathi

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

**como** moderador
**quiero** poder borrar un bar existente
**para** que no pueda ser sugerido por la aplicación a los usuarios

_CRITERIO DE ACEPTACION:_

1. El moderador puede seleccionar un bar que este en el catalogo para eliminarlo
2. Si un usuario busca el bar eliminado este no deberá aparecer
3. Si un usuario esta puntuando o comentando cuando se elimina el bar este recibirá una notificación comunicando que dicha acción ya no esta disponible

**como** moderador
**quiero** poder editar la información de un bar existente
**para** actualizar datos incorrectos o incompletos

_CRITERIO DE ACEPTACION:_

1. El moderador puede seleccionar un bar que este en el catalogo para editarlo
2. Si un usuario busca el bar editado este aparecerá con los datos actualizados
3. Si se cambia la dirección del bar, cuando un usuario consulte como llegar al mismo se cargará el recorrido actualizado.
4. Si se cambia la dirección dele bar, cuando un usuario busque por bares cercanos el bar aparecerá o no según su nueva dirección y no la antigua.
