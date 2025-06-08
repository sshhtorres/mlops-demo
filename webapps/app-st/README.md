# Aplicación web de interacción con modelos

**Ejecución en local utilizando ambiente virtual:**

1. Configurar ambiente virtual local con `uv` ([https://docs.astral.sh/uv/](https://docs.astral.sh/uv/)):
    ```sh
    # multiplataforma 
    uv sync
    ```

2. Definir variables de ambiente e iniciar servicio:
    ```bash
    export ML_IRIS_SERVICE_URL=
    export ML_MNIST_SERVICE_URL=
    uv run streamlit run src/app.py
    ```

    La aplicación inicia por defecto en el puerto 8501: [http://localhost:8501](http://localhost:8501)

**Ejecución en local utilizando Docker:**

```bash
# construir imagen
docker build -t app-st .

# definir variables de ambiente
ML_IRIS_SERVICE_URL=
ML_MNIST_SERVICE_URL=

# ejecutar contenedor
docker run --rm --name app \
    -e ML_IRIS_SERVICE_URL="$ML_IRIS_SERVICE_URL" \
    -e ML_MNIST_SERVICE_URL="$ML_MNIST_SERVICE_URL" \
    -p 8501:8501 \
    app-st
```

**Consideraciones:**

Respecto al estado de sesión de la aplicación `st.session_state` y sus correspondientes llaves y valores (keys, values):
- en [states.py](./src/states.py) se definen mappings de llaves de estado de sesión de `streamlit` para centralizar la definición de llaves y reforzar el acceso a ellas a través de propiedades definidas en modelos de `pydantic`.
- considerando que `streamlit` requiere inicializar el estado de sesión para cada llave, se puede inicializar como valor por defecto en el mapeo de estado de sesión en [states.py](./src/states.py), o manualmente en el componente; ambas opciones son mutuamente excluyentes dado que `streamlit` exige una única inicialización de valor de estado de sesión por llave.

Respecto a nuevas configuraciones y módulos de servicios ML:
- el identificador de la configuración de servicio ML en [src/config.py](./src/config.py) y el nombre del módulo en [src/components/ml/](./src/components/ml) deben coincidir, por ejemplo, en el caso de `iris` y `mnist`.
- el módulo en [src/components/ml/](./src/components/ml) debe contener una función `render()` para renderizar el componente.
- es recomendable definir la estructura de estados en [states.py](./src/states.py) según se utiliza en el módulo.

**Referencias:**

Respecto a declaración de componentes personalizados de Streamlit:
- Documentación: https://docs.streamlit.io/develop/concepts/custom-components
- Plantilla: https://github.com/streamlit/component-template
- Ejemplo plantilla vanilla (sin React): https://github.com/streamlit/component-template/blob/master/template-reactless/my_component/frontend/src/index.tsx
- CDN con demo en JSFiddle para ESM: https://www.jsdelivr.com/package/npm/streamlit-component-lib
