# MyFirstGame
## El juego

El juego consiste en disparar a triangulos que decienden. Estilo space invaders con figuras gemetricas.
Para el heroe permite tener un poligono desde 4 lados hasta 7 lados en tres colores. Estos parametros se pueden configurar al inicio del juego o despues de terminar un nivel.
Cada menu para configurar estso parametros esta diseñado para usarse presionando teclas. No hay necesidad de usar el mouse.
El juego cuenta con 3 niveles. Cada nivel tiene un numero primo de la malos, mas un jefe.
A los triangulos (los malos) hay que disparales 5 veces para que desaparezcan. Los jefes (triagulos mas grandes) hay que dispararles 50 veces.
AL estrellar el heroe con uno de los malos, este desaparece. Sin embargo si el heroe se estrella 4 veces es Game Over.

## Carateristicas de funcionalidad

Para el manejo de los malos y los disparos se usan diccionarios.
Con estos diccionarios en una tupla se guarda el objeto surface, la posicion, y una funcion generadora que permitira calcular la proxima posicion.
Estos parametros, o los que sean necesarios se pueden acceder con un nombre. El nombre se seleccionado revisando algun parametro de esta tupla y guardandolo en una lista.
**EJEMPLO:** *Para una colision entre el heroe y los malos se recorre el diccionario de los malos donde se guardaron en un argumento de la tupla las superficies.*
*Se recorre usando la funcion .items() que devuelve una tupla de llave, argumento. Se extrae del argumento la superficie, se genera un objeto tipo rect, y se revisa si existe colision.*
*En caso de que exista, con el indice devuelto por la fucnion para revisar colisiiones de PYGAME ,se busca la llave y se elimina con esta el par llave argumento del diccionaro de malos*
Al estar guardados en un diccionario, una vez que el objeto "muere", o sus posiciones salen del recuadro estos se pueden eliminar lo que ahorra espacio en memoria.
De ser necesario se genera otro malo hasta que el heroe haya eliminado los suficientes para avanzar de nivel.
Respecto al movimiento, para poder hacer que los elementos se muevan automaticos, se usa una fucncion generadora asociada a la superficie.
Esta funcion al usar **Yield** en vez de **Return** permite detener la ejecucion del codigo y devolver un valor.
Asi con el uso de una itereacion se puede asegurar que las posiciones siempre den un valor, y que si esta fuera de la pantalla de un valor predeterminado que permita identificar y eliminar de la lista de lementos usados.
Como ultimo elemnto resaltable de la fucnionalidad, se usa el objeto tiempo de PYGAME, se cuentan las vueltas del loop de juego, y se usan funciones de la libreria random.
Haciendo uso de estos elemntos y la funcion basica modulo **%** de python, se da una apariencia mas pausada al juego y se da pie para que la aparicion de los malos sea paulatina y con colores aleatorios. 

