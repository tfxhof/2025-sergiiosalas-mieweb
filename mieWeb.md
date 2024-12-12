# Herramienta web para la comparación de la respuesta electromagnética de distintos materiales calculada con la solución Mie

La teoría o solución de Mie ofrece una solución analítica a las ecuaciones de Maxwell para la dispersión (scattering) de la radiación electromagnética por partículas esféricas. Esta solución permite calcular los campos eléctricos y magnéticos producidos fuera y dentro de un objeto esférico sobre el que se hace incidir dicha radiación (luz, por ejemplo).

Las características del material de la esfera afectan a la dispersión que se obtiene, siendo entonces posible obtener una dispersión deseada para una aplicación concreta mediante la selección del material adecuado. No obstante, el uso de las fórmulas de Mie para esta selección puede ser tedioso ya que, aunque existen varias librerías software que implementan estas fórmulas, estas requieren de conocimientos de programación, tanto para la ejecución de las fórmulas, como para la obtención de las características ópticas de los materiales a probar, normalmente extraídas de libros, artículos científicos, o de bases de datos como RefractiveIndex.Info (https://refractiveindex.info/).

Este trabajo busca desarrollar una herramienta web que sea capaz de permitir a usuarios sin conocimientos técnicos en programación comparar la difracción obtenida al aplicar Mie sobre distintos materiales. La herramienta, a grandes rasgos, permitirá a sus usuarios el siguiente proceso:

1. Seleccionar materiales del catálogo ofrecido por RefractiveIndex.info. En el repositorio de código fuente de dicha base de datos existen diferentes formas de acceder al catálogo de materiales (https://github.com/polyanskiy/refractiveindex.info-database).

2. Calcular la absorción y dispersión obtenida para cada material utilizando una implementación de Mie. Existen numerosas librerías para realizar este cálculo (e.g. https://miepython.readthedocs.io/en/latest/), por lo que parte del trabajo será también seleccionar aquella que mejor se adapte a las necesidades del proyecto.

3. Mostrar gráficamente los resultados obtenidos para cada material, de forma que un usuario pueda compararlos.

4. Permitir exportar o compartir la información obtenida.

El usuario de la herramienta podrá añadir o eliminar materiales de la comparativa en cualquier momento, y la herramienta deberá dinámicamente responder a estos cambios actualizando la información mostrada.

Por las librerías utilizadas, este trabajo se realizará prácticamente en su totalidad en Python, existiendo la posibilidad también de que sea necesario realizar un pequeño desarrollo web para la creación del cliente. Este desarrollo web podría realizarse también mediante frameworks de Python como Panel (https://panel.holoviz.org/).
