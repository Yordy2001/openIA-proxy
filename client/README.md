# Cliente React - Análisis Contable con IA

Este es un cliente React que permite subir archivos Excel y obtener análisis contable automático usando inteligencia artificial.

## Características

- 📁 Subida de archivos Excel (.xlsx, .xls)
- 🤖 Análisis automático con IA
- 📊 Visualización clara de resultados
- 🎯 Hallazgos categorizados por severidad
- 💡 Recomendaciones priorizadas
- 🔄 Interfaz intuitiva y responsive

## Instalación

1. Navega al directorio del cliente:
   ```bash
   cd client
   ```

2. Instala las dependencias:
   ```bash
   npm install
   ```

## Uso

1. Asegúrate de que el backend esté funcionando en `http://localhost:8000`

2. Inicia el cliente React:
   ```bash
   npm start
   ```

3. Abre tu navegador en `http://localhost:3000`

4. Sube archivos Excel y obtén análisis automático

## Estructura del Proyecto

```
client/
├── public/
│   └── index.html
├── src/
│   ├── App.js              # Componente principal
│   ├── App.css             # Estilos de App
│   ├── index.js            # Punto de entrada
│   ├── index.css           # Estilos globales
│   ├── apiService.js       # Servicio para comunicación con backend
│   ├── FileUpload.js       # Componente para subir archivos
│   └── ResultsDisplay.js   # Componente para mostrar resultados
├── package.json
└── README.md
```

## Configuración

### Variables de Entorno

Puedes crear un archivo `.env` en el directorio `client/` con las siguientes variables:

```env
REACT_APP_API_URL=http://localhost:8000
```

### Proxy

El `package.json` incluye configuración de proxy para desarrollo:

```json
{
  "proxy": "http://localhost:8000"
}
```

## Funcionalidades

### Subida de Archivos

- Soporte para múltiples archivos Excel
- Validación de tipos de archivo
- Arrastrar y soltar archivos
- Prompt personalizado opcional

### Visualización de Resultados

- **Resumen**: Descripción general del análisis
- **Hallazgos**: Errores, advertencias e información
- **Recomendaciones**: Sugerencias categorizadas por prioridad
- **Estadísticas**: Resumen numérico de hallazgos

### Tipos de Hallazgos

- 🔴 **Error**: Problemas críticos que requieren atención inmediata
- 🟡 **Warning**: Advertencias que deben revisarse
- 🔵 **Info**: Información general o sugerencias menores

### Niveles de Severidad

- **Alta**: Requiere acción inmediata
- **Media**: Debe abordarse pronto
- **Baja**: Puede abordarse cuando sea conveniente

## Desarrollo

### Scripts Disponibles

- `npm start`: Inicia el servidor de desarrollo
- `npm run build`: Construye la aplicación para producción
- `npm test`: Ejecuta las pruebas
- `npm run eject`: Expone la configuración de webpack

### Tecnologías Utilizadas

- **React 18**: Framework principal
- **Axios**: Cliente HTTP para comunicación con backend
- **CSS3**: Estilos responsivos
- **HTML5**: Estructura semántica

## Solución de Problemas

### Error de Conexión

Si no puedes conectar con el backend:

1. Verifica que el backend esté ejecutándose en `http://localhost:8000`
2. Revisa la configuración de CORS en el backend
3. Verifica las variables de entorno

### Problemas de Subida

Si los archivos no se suben correctamente:

1. Verifica que sean archivos Excel válidos (.xlsx, .xls)
2. Revisa el tamaño del archivo (límite en el backend)
3. Comprueba la conexión de red

### Errores de Análisis

Si el análisis falla:

1. Verifica que el backend tenga configurada la API de IA
2. Revisa que los archivos Excel tengan el formato correcto
3. Comprueba los logs del backend para más detalles

## Próximas Mejoras

- [ ] Historial de análisis
- [ ] Exportación de resultados
- [ ] Más tipos de archivo (CSV, ODS)
- [ ] Configuración de usuario
- [ ] Modo oscuro
- [ ] Notificaciones push

## Licencia

Este proyecto es privado y está desarrollado para análisis contable automatizado. 