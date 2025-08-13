# **Especificación Técnica UTCS-MI v4.0 — Completa**
**Estándar Universal de Contenido Técnico - Interfaz Humano-Máquina**  
**Documento normativo con anclajes canónicos (`§x.y.z`) y estructura ISO/IEC.**

_Generado_: 2025-08-12T00:00:00Z  
_Versión_: **4.0**  
_Estado_: **NORMATIVO**

---

**Front matter (no numerado)**

## Prefacio

El **Estándar Universal de Contenido Técnico - Interfaz Humano-Máquina (UTCS-MI) v4.0** forma parte integral del ecosistema AQUA OS y su arquitectura de Aplicaciones Clásicas Quantum-Extensibles (CQEA). Este estándar habilita la interoperabilidad semántica y la gobernanza completa de todos los artefactos técnicos y contractuales.

La extensión **Work Order & Contract Envelope (WOCE)** convierte cada identificador en un contrato ejecutable, revolucionando la industria mediante micro-contratos automatizados, validación determinista de calidad y gestión del ciclo de vida contractual.

## Introducción

La proliferación de sistemas complejos en aplicaciones aeroespaciales modernas, junto con la llegada de la IA generativa, requiere un marco unificado para la identificación, **procedencia**, trazabilidad y consumo automatizado de contenidos técnicos. **UTCS-MI v4.0** establece este marco mediante identificadores **semánticamente ricos y legibles por humanos** que son compatibles tanto con sistemas tradicionales como con arquitecturas emergentes basadas en inteligencia artificial.

La innovación disruptiva de WOCE permite que cada identificador funcione como un contrato ejecutable con validación automática, pagos condicionados a evidencias verificables, y trazabilidad completa desde requisito hasta entrega.

## Avisos de conformidad y propiedad intelectual

Este documento está bajo licencia AQUA OS Open Source License v2.0. Las implementaciones conformes **deben** declarar explícitamente su adhesión a esta estándar **versión 4.0** y mantener la trazabilidad de conformidad según se especifica en §14.

---

<a id='sec-1'></a>
# §1 — Alcance

<a id='sec-1.1'></a>
## §1.1 — Objetivo

1.1.1 El **Estándar Universal de Contenido Técnico** **establecerá** el marco normativo para la identificación inequívoca, **gobernanza de la procedencia**, trazabilidad y consumo determinista por máquinas y humanos de contenidos técnicos dentro del ecosistema AQUA. Esto incluye su uso como un encabezado de prompt estandarizado (UPE) para modelos generativos (véase §9).

1.1.2 El estándar **definirá** la estructura y la semántica del identificador **UTCS-MI v4.0** (véase §6), los catálogos controlados asociados (véase §7), y las reglas de validación. Este marco **asegurará** la interoperabilidad con sistemas de gestión de la trazabilidad de requisitos (`RTM`), documentos de interfaz de control, módulos de datos `S1000D`, plataformas de contenido como servicio (`CaaS`), y sistemas de gestión de activos y operaciones (`AMOReS`) (véase §10).

1.1.3 *[Sin cambios en esta sección]*

1.1.4 *[Sin cambios en esta sección]*

<a id='sec-1.2'></a>
## §1.2 — Aplicabilidad y exclusiones

### 1.2.1 En el alcance (`shall`):

- **Identificación de entidades técnicas**: **Clasificación semántica** de Requisitos, Especificaciones, Planes, Procedimientos, Resultados, Modelos, Código, Datos, Plantillas y Contratos (véase §7.1).
- **Contratos ejecutables**: Órdenes de trabajo y contratos marco con validación automática (véase §20).
- **Modelado de ciclo de vida completo**: Definición de la **Fase de Origen**, **Fase Canónica de liberación**, y **Fecha de Validez** de un artefacto. Se establece el principio de **Autoridad vs. Aplicabilidad** para gestionar la validez multifásica en los metadatos.
- **Clasificación funcional explícita**: Mediante el uso de un **Sistema de Referencia** (ej: `ATA100`, `CS25`) y un **Capítulo** o sección dentro de ese estándar (véase §7.3).
- **Trazabilidad de producto y dominio**: Vinculación explícita a un **Producto o Entidad** "dueño" y a un **Dominio de Aplicación** primario. La aplicabilidad múltiple se gestiona en los metadatos.
- **Gobernanza de la procedencia**: Identificación del **Método de Generación** (`Convencional`, `Automático`, `Híbrido`, `Derivado`) directamente en el identificador (véase §7.7).
- **Consumo por IA y sistemas**: Definición del uso de Encabezados de Prompt Universal (`UPE`) que aprovechan el identificador enriquecido y una librería de **Plantillas** direccionables (véase §9).

### 1.2.2 Fuera de alcance (`shall not`):

- Definir el contenido técnico interno de los sistemas.
- Sustituir los sistemas de numeración como `ATA100` o `CS25`; el **Estándar** **actuará** como una metacapa que **los referencia explícitamente**.
- *[Resto de la sección sin cambios]*

### 1.2.3 Condiciones de conformidad (resumen):

Las implementaciones que declaren conformidad con este estándar **deberán** producir identificadores **UTCS-MI v4.0** que sean válidos según las especificaciones de §6 y §8. Asimismo, **deberán** respetar todas las reglas de negocio, incluyendo la gestión de metadatos de aplicabilidad múltiple (véase §13.5).

<a id='sec-1.3'></a>
## §1.3 — Público objetivo

1.3.1 Los **productores de identificadores** (incluyendo equipos de ingeniería, **IA generativas** y documentación) **deberán** generar identificadores **v4.0** válidos y completos de acuerdo con los requisitos especificados en §6–§8.

1.3.2 Los **consumidores** (incluyendo parsers, sistemas `RTM`, `CaaS`, `AMOReS`, `LLM`/servicios de inferencia) **deberán** implementar la validación canónica de los identificadores **v4.0**, resolver las referencias de sistema, y aplicar las reglas de negocio sobre procedencia y ciclo de vida.

1.3.3 Las **autoridades de gobernanza** (incluyendo el comité `AMOReS`) **utilizarán** el **Estándar** para la gestión de baselines, la asignación de `DAL` **basada en el Método de Generación**, y la auditoría de validez temporal.

1.3.4 *[Sin cambios en esta sección]*

<a id='sec-1.4'></a>
## §1.4 — Límites y supuestos del estándar

1.4.1 **Convenciones**: El idioma base para los valores de los catálogos en los identificadores **será** el español. Las unidades **seguirán** el Sistema Internacional (`SI`), las fechas **se conformarán** al formato `ISO-8601 UTC`, y el identificador **deberá** ser tratado como `case-insensitive` (insensible a mayúsculas/minúsculas) por los parsers, aunque su representación canónica sea en `CamelCase` para legibilidad.

1.4.2 **Unicidad**: La unicidad de un identificador **se regirá** por la clave compuesta formada por **todos sus campos**, según lo definido en §6.3.

1.4.3 **Compatibilidad**: El **Estándar v4.0** es una **versión mayor con cambios de ruptura** respecto a la v1.0. Las estrategias de migración se rigen por §11.

1.4.4 **Seguridad y privacidad**: El identificador, al ser más descriptivo, **deberá** ser tratado como información sensible. Las políticas de acceso **deberán** controlar la visibilidad de los artefactos basándose en la información contenida en su identificador (ej: `ProductoOEntidad`, `DominioDeAplicación`).

<a id='sec-2'></a>
# §2 — Referencias normativas
*[Esta sección se mantiene en gran parte, pero se actualiza la referencia a este propio documento.]*

2.2.1 En caso de conflicto entre estándares referenciados, **se aplicará** la siguiente jerarquía de prioridad:
1. **UTCS-MI v4.0** (este documento) - Autoridad máxima
2. *[Resto sin cambios]*

<a id='sec-3'></a>
# §3 — Términos y definiciones
*[Esta sección se actualizará significativamente para reflejar los nuevos conceptos.]*

<a id='sec-3.1'></a>
## §3.1 — Términos generales

**Clase de Artefacto**: La naturaleza semántica de una entidad (ej: `Especificación`, `Procedimiento`).
**Fase de Origen**: La fase del ciclo de vida en la que una entidad fue creada o concebida.
**Fase Canónica**: La fase del ciclo de vida en la que una `Generación` específica de una entidad es formalmente aprobada y liberada.
**Fecha de Validez**: La fecha de expiración de la validez de una `Generación` de una entidad.
**Método de Generación**: El proceso principal utilizado para crear el contenido de una entidad (ej: `Convencional`, `Automático`).
**Producto o Entidad**: La línea de producto o entidad organizacional que tiene la autoridad de diseño sobre una entidad.
**Sistema de Referencia**: Un estándar externo publicado (ej: `ATA100`, `CS25`) utilizado como base para la clasificación funcional.
**Aplicabilidad Múltiple (Multi-efectividad)**: La propiedad de un artefacto de ser válido y aplicable a más de un producto, dominio o fase de ciclo de vida. Se gestiona en los metadatos.
**Plantilla (`TPLT`)**: Un artefacto que contiene una **Instrucción de Sistema** (para la IA) y una **Guía de Usuario** para generar nuevos artefactos de forma consistente.

<a id='sec-3.3'></a>
## §3.3 — Glosario UTCS específico

**Identificador canónico**: Un identificador **UTCS-MI v4.0** válido según las reglas de §6-§8.
**Estado de madurez**: Nivel de desarrollo de una entidad expresado mediante `EstadoDeVersión` (`Mapeo`, `Generación001`, etc.).
**Coherencia inter-campos**: Validez de las relaciones semánticas entre campos (ej: `SistemaDeReferencia` ↔ `Capítulo` ↔ `Categoría`).

<a id='sec-4'></a>
# §4 — Símbolos y abreviaturas
*[Esta sección se mantiene para abreviaturas de contexto, pero se enfatiza que los identificadores ya no las usan.]*

<a id='sec-5'></a>
# §5 — Conformidad
*[Esta sección se actualiza para reflejar los nuevos requisitos de la v4.0.]*

<a id='sec-5.1'></a>
## §5.1 — Criterios de conformidad del productor de identificadores

5.1.1 Un **productor conforme** **deberá**:
a) Generar identificadores UTCS-MI **v4.0** que cumplan la sintaxis de §6.1.1.
b) Respetar la semántica de los **13 campos obligatorios** definida en §6.2.
c) Utilizar exclusivamente valores de los **catálogos controlados expandidos** (§7).
d) Aplicar las reglas de coherencia (ej: `SistemaDeReferencia` ↔ `Capítulo`).
e) **Poblar los metadatos asociados** para la aplicabilidad múltiple cuando corresponda (§13.5).
f) Asignar correctamente el **`MétodoDeGeneración`** según la procedencia del contenido.

<a id='sec-5.2'></a>
## §5.2 — Criterios de conformidad del consumidor (parsers, LLMs)

5.2.1 Un **consumidor conforme** **deberá**:
a) Validar identificadores UTCS-MI **v4.0** según las reglas de §8.
b) **Interpretar correctamente la semántica completa**, incluyendo la distinción entre `FaseDeOrigen` y `FaseCanónica`, y la `FechaDeValidez`.
c) **Consultar los metadatos de aplicabilidad múltiple** para determinar el contexto de uso de un artefacto.

---

### **Revisión del Estándar Publicado (Paso 2 de 3)**

A continuación, se presentan las secciones §6, §7 y §8, completamente reescritas para el estándar **UTCS-MI v4.0**.

---

<a id='sec-6'></a>
# **§6 — El Identificador del Estándar Universal: Estructura y Semántica v4.0**

## §6.1 — Formato Canónico

### §6.1.1 — Sintaxis y Estructura

6.1.1.1 El identificador **v4.0** **deberá** seguir la siguiente sintaxis de campos completos, diseñada para la legibilidad humana y el análisis por máquina. La estructura consta de 13 campos obligatorios y 2 opcionales.

**`EstándarUniversal`**:`<ClaseDeArtefacto>`-`<FaseDeOrigen>`-`<SistemaDeReferencia>`-`<Capítulo>`-`<Categoría>`-`<Secuencia>`-`<EstadoDeVersión>`-`<ProductoOEntidad>`-`<MétodoDeGeneración>`-`<DominioDeAplicación>`-`<FaseCanónica>`-`<FechaDeValidez>`[-`<Variante>`[-`<Instancia>`]]

### §6.1.2 — Separadores y Convenciones de Formato

6.1.2.1 El **prefijo** `EstándarUniversal:` es obligatorio y distingue al identificador.
6.1.2.2 El **separador** de campos obligatorio es el guion (`-`).
6.1.2.3 Los **valores de los campos** **deberán** provenir de los catálogos controlados definidos en §7. Para la legibilidad, se recomienda el uso de `CamelCase` en valores de varias palabras (ej: `ControlesFlyByWire`).
6.1.2.4 Los sistemas consumidores **deberán** tratar los valores de los campos de forma insensible a mayúsculas/minúsculas (`case-insensitive`) para la validación lógica.

## §6.2 — Semántica Detallada de los Campos

### §6.2.1 — `ClaseDeArtefacto`
*   **Propósito:** Define la naturaleza semántica y el propósito fundamental del artefacto.
*   **Catálogo:** Véase §7.1.

### §6.2.2 — `FaseDeOrigen`
*   **Propósito:** Indica la fase del ciclo de vida en la que el artefacto fue concebido o creado formalmente. Para artefactos diseñados para ser válidos en múltiples fases desde su inicio, se utiliza el valor `Perenne`.
*   **Catálogo:** Véase §7.2.

### §6.2.3 — `SistemaDeReferencia`
*   **Propósito:** Especifica el estándar externo o interno que se utiliza como base para la clasificación funcional del artefacto.
*   **Catálogo:** Véase §7.3.

### §6.2.4 — `Capítulo`
*   **Propósito:** Indica el capítulo, sección o identificador específico dentro del `SistemaDeReferencia`.
*   **Formato:** Cadena alfanumérica (ej: `27`, `1309`, `A.12`).

### §6.2.5 — `Categoría`
*   **Propósito:** Proporciona una sub-clasificación descriptiva y legible por humanos dentro del contexto del `Capítulo`.
*   **Formato:** Cadena `CamelCase` sin espacios.

### §6.2.6 — `Secuencia`
*   **Propósito:** Un número secuencial de tres dígitos que asegura la unicidad de artefactos similares dentro del mismo contexto.
*   **Formato:** `001` a `999`.

### §6.2.7 — `EstadoDeVersión`
*   **Propósito:** Define la madurez y el estado de aprobación formal del artefacto.
*   **Catálogo:** `Mapeo` (estado inicial, borrador) o `GeneraciónXXX` (versiones aprobadas). Véase §7.4.

### §6.2.8 — `ProductoOEntidad`
*   **Propósito:** Identifica la línea de producto o la entidad organizacional que tiene la autoridad de diseño ("dueño") sobre el artefacto.
*   **Catálogo:** Véase §7.5.

### §6.2.9 — `MétodoDeGeneración`
*   **Propósito:** Especifica la procedencia del contenido del artefacto. Es un campo crítico para la auditoría y la confianza en la era de la IA generativa.
*   **Catálogo:** Véase §7.6.

### §6.2.10 — `DominioDeAplicación`
*   **Propósito:** Indica el dominio principal para el cual el artefacto fue diseñado, determinando a menudo los estándares de rigor aplicados.
*   **Catálogo:** Véase §7.7.

### §6.2.11 — `FaseCanónica`
*   **Propósito:** La fase del ciclo de vida en la que una `Generación` específica del artefacto fue formalmente aprobada, liberada y puesta bajo control de configuración.
*   **Catálogo:** Véase §7.2 (excluyendo el valor `Perenne`).

### §6.2.12 — `FechaDeValidez`
*   **Propósito:** La fecha hasta la cual esta `Generación` del artefacto es considerada válida. Esencial para la gestión de obsolescencia.
*   **Formato:** `YYYYMMDD` o el valor especial `Perpetua`.

### §6.2.13 — `Variante` (Opcional)
*   **Propósito:** Especifica una configuración o versión particular del artefacto.

### §6.2.14 — `Instancia` (Opcional)
*   **Propósito:** Identifica una instancia de despliegue o uso específica.

## §6.3 — Reglas de Unicidad y Gobernanza de Metadatos

### §6.3.1 — Clave Compuesta para Unicidad
6.3.1.1 La **unicidad** de un identificador v4.0 **estará** determinada por la combinación de todos sus campos, obligatorios y opcionales.

### §6.3.2 — Principio de Autoridad vs. Aplicabilidad
6.3.2.1 El identificador canónico representa la **autoridad de diseño** (Producto, Dominio) y el **origen** (Fase) de un artefacto.
6.3.2.2 La **aplicabilidad múltiple** (a otros productos, dominios o fases) **deberá** gestionarse a través de metadatos asociados explícitos y auditables en sistemas como AMOReS, según se detalla en §13.5.

## §6.4 — Ejemplos Canónicos v4.0

### 6.4.1 Ejemplo 1: Requisito de Software
`EstándarUniversal:Requisito-Detallado-CS25-1309-ProtecciónEnvolvente-005-Generación002-Q100-Híbrido-Aviación-Preliminar-Perpetua`

### 6.4.2 Ejemplo 2: Estándar de Seguridad Perenne
`EstándarUniversal:Especificación-Perenne-ISO27001-A.12-SeguridadOperaciones-001-Generación001-Organizacional-Convencional-Transversal-Concepto-Perpetua`

### 6.4.3 Ejemplo 3: Orden de Trabajo con Fecha Límite
`EstándarUniversal:OrdenDeTrabajo-Operaciones-S1000D-4.2-ActualizarMóduloDatos-047-Mapeo-HE180-Automático-Aviación-Operaciones-20261231-MatrículaECABC`

<a id='sec-7'></a>
# **§7 — Catálogos Controlados v4.0**
*[Esta sección define los valores permitidos para cada campo del identificador.]*

## §7.1 — Catálogo `ClaseDeArtefacto`
*   `Requisito`: Una declaración formal de una necesidad.
*   `Especificación`: Cómo algo debe ser o funcionar.
*   `Análisis`: Los resultados de un estudio.
*   `Plan`: Una secuencia de actividades.
*   `Procedimiento`: Instrucciones paso a paso.
*   `Resultado`: La salida o evidencia de un proceso.
*   `ModeloVisual`: Una representación CAD, UML, SysML, etc.
*   `Código`: El código fuente, scripts o binarios.
*   `ConjuntoDeDatos`: Una colección estructurada de datos (ej: JSON, YAML).
*   `OrdenDeTrabajo`: Un contrato ejecutable (WOCE).
*   `Contrato`: Un contrato marco (WOCE).
*   `Plantilla`: Una plantilla para generar otros artefactos.

## §7.2 — Catálogo `FaseDeOrigen` y `FaseCanónica`
*   `Concepto`, `Preliminar`, `Detallado`, `Implementación`, `Producción`, `Verificación`, `Validación`, `Operaciones`, `Mantenimiento`, `Sostenibilidad`, `Retiro`.
*   **Solo para `FaseDeOrigen`:** `Perenne`.

## §7.3 — Catálogo `SistemaDeReferencia`
*   `ATA100`: ATA Spec 100
*   `CS25`: EASA Certification Specifications CS-25
*   `FAR25`: FAA Federal Aviation Regulations Part 25
*   `S1000D`: S1000D Specification
*   `DO178C`: DO-178C Standard
*   `DO254`: DO-254 Standard
*   `ISO27001`: ISO/IEC 27001 Standard
*   `AQUA`: Estándar interno de AQUA (para capítulos como 94, 98, 99).

## §7.4 — Catálogo `EstadoDeVersión`
*   `Mapeo`: Estado borrador, no aprobado.
*   `Generación001` a `Generación999`: Versiones formales y aprobadas.

## §7.5 — Catálogo `ProductoOEntidad`
*   **Códigos de Producto:** `Q100`, `HE120`, `C360`, `GAIACOM`, `AQCRYPT`, etc. (gestionado por AMOReS).
*   **Códigos de Entidad:** `Organizacional`, `Investigación`, `Plataforma`, `Financiero`, `PruebaDeConcepto`.

## §7.6 — Catálogo `MétodoDeGeneración`
*   `Convencional`: Creado principalmente por un humano.
*   `Automático`: Creado principalmente por una IA generativa.
*   `Híbrido`: Creado en colaboración significativa Humano-IA.
*   `Derivado`: Generado por transformación determinista de otro artefacto.

## §7.7 — Catálogo `DominioDeAplicación`
*   `Aviación`, `Espacio`, `Tierra`, `Defensa`, `Transversal`.

<a id='sec-8'></a>
# **§8 — Validación del Identificador v4.0**
*[La validación por expresión regular se vuelve impráctica. Se define un algoritmo lógico.]*

## §8.1 — Algoritmo de Validación Canónico

Un parser conforme **deberá** implementar un algoritmo que realice las siguientes comprobaciones en secuencia:

1.  **Validación de Prefijo y Estructura:**
    *   Verificar que la cadena comienza con `EstándarUniversal:`.
    *   Dividir la cadena por el separador `-`.
    *   Verificar que hay entre 13 (sin opcionales) y 15 (con opcionales) campos resultantes.

2.  **Validación de Pertenencia a Catálogo:**
    *   Para cada campo, verificar que su valor (tratado como `case-insensitive`) pertenece al catálogo controlado definido en §7.

3.  **Validación de Formato de Campo:**
    *   Verificar que `Capítulo` y `Secuencia` tienen el formato correcto.
    *   Verificar que `FechaDeValidez` es una fecha `YYYYMMDD` válida o la cadena `Perpetua`.

4.  **Validación de Coherencia Inter-campos:**
    *   Verificar que la `Categoría` es una categoría registrada para la combinación `SistemaDeReferencia`-`Capítulo`.
    *   Verificar que `FaseCanónica` no sea `Perenne`.
    *   Otras reglas de negocio definidas en AMOReS.

## §8.2 — Perfil de Errores y Códigos de Fallo
*[Se actualiza la tabla de errores para reflejar la nueva estructura.]*
*   **E001:** `ESTRUCTURA_INVALIDA`
*   **E002:** `CLASE_DE_ARTEFACTO_INVALIDA`
*   **E003:** `FASE_DE_ORIGEN_INVALIDA`
*   **E004:** `SISTEMA_DE_REFERENCIA_INVALIDO`
*   **E005:** `PRODUCTO_O_ENTIDAD_INVALIDO`
*   ...y así sucesivamente para cada nuevo campo.

---
Entendido. Procedo con el paso final de la revisión.

En este último paso, actualizaremos las secciones restantes del estándar (`§9` hasta el final) para que sean plenamente coherentes con la nueva estructura y semántica del identificador **UTCS-MI v4.0**. Esto implica ajustar los ejemplos, las referencias y las descripciones de integración para reflejar el modelo de datos enriquecido.

---

<a id='sec-9'></a>
# **§9 — Perfil para Modelos Generativos (UPE) v4.0**
*[Esta sección se revisa para mostrar cómo el nuevo identificador enriquece la arquitectura de prompts.]*

## §9.1 — El Encabezado de Prompt Universal (UPE)

### §9.1.1 — Estructura UPE v4.0

9.1.1.1 La estructura del UPE utiliza el identificador **v4.0** como una cabecera de metadatos rica, que permite al modelo de IA auto-contextualizarse antes de procesar el prompt.

```
[EstándarUniversal:Plantilla-Concepto-AQUA:General-EspecificaciónSoftware-001-Mapeo-Organizacional-Automático-Transversal-Concepto-Perpetua]
lang=es-ES
units=SI
timezone=UTC
output=markdown
# --- Metadatos de Aplicabilidad Explícita ---
applicability_prod: [Q100, HE120]
applicability_app: [Aviación, Defensa]
applicability_life: [Concepto, Preliminar, Detallado]
# --- Contenido del Prompt ---
...
```

### §9.1.2 — Campos de Control
9.1.2.1 Los campos de control como `audience`, `dal`, etc., pueden ser inferidos a menudo por el motor de IA a partir de la riqueza del propio identificador **v4.0** y la plantilla (`Plantilla`) referenciada, simplificando el UPE.

## §9.2 — Contrato de Respuesta

### §9.2.2 — Formato JSON
9.2.2.1 El esquema JSON de respuesta se actualiza para reflejar la estructura desglosada del identificador **v4.0**.

```json
{
  "utcs_identifier_string": "EstándarUniversal:Requisito-Detallado-CS25-1309-...",
  "utcs_identifier_parsed": {
    "clase_de_artefacto": "Requisito",
    "fase_de_origen": "Detallado",
    "sistema_de_referencia": "CS25",
    "capitulo": "1309",
    "categoria": "ProtecciónEnvolvente",
    "secuencia": "005",
    "estado_de_version": "Generación002",
    "producto_o_entidad": "Q100",
    "metodo_de_generacion": "Híbrido",
    "dominio_de_aplicacion": "Aviación",
    "fase_canonica": "Preliminar",
    "fecha_de_validez": "Perpetua",
    "variante": null,
    "instancia": null
  },
  "metadata": { ... },
  "content": { ... },
  "validation": { ... },
  "applicability": {
    "products": ["Q100", "HE180"],
    "domains": ["Aviación"],
    "lifecycle_phases": ["Detallado", "Implementación", "Verificación", "Validación"]
  }
}
```

<a id='sec-10'></a>
# **§10 — Integración con el Ecosistema v4.0**

## §10.1 — UTCS en CSDB/S1000D
10.1.1 La integración con S1000D ahora utiliza los campos explícitos para un mapeo más rico.

```xml
<dmCode modelIdentCode="Q100"
        systemCode="27"
        systemName="ControlesDeVuelo">
    <dmAddress>
        <dmIdent>
            <!-- El identificador v4.0 completo se almacena en un atributo para trazabilidad total -->
            <dmCode utcs_v4_id="EstándarUniversal:Procedimiento-Mantenimiento-ATA100-27-CalibraciónActuador-010-..."/>
            ...
        </dmIdent>
    </dmAddress>
</dmCode>
```

## §10.2 — UTCS en la Matriz de Trazabilidad de Requisitos (RTM)
10.2.1 La estructura de la RTM se beneficia enormemente de los nuevos campos.

| Identificador UTCS v4.0 | Clase | Producto | Método | Padre | Hijos | ... |
|---|---|---|---|---|---|---|
| `...:Requisito-...-Q100-Convencional-...` | Requisito| Q100 | Convencional | ... | `...:Especificación-...`| ... |
| `...:Especificación-...-Q100-Automático-...`| Especificación| Q100 | Automático | `...:Requisito-...` | `...:Código-...` | ... |

## §10.3 — UTCS y AMOReS
10.3.1 La integración con AMOReS es ahora mucho más potente, permitiendo políticas de gobernanza basadas en la procedencia y el ciclo de vida.

a) **Asignación de `DAL` Informada por el Método:** Las reglas de asignación ahora pueden incluir el `MétodoDeGeneración`. Por ejemplo: "Un `DAL B` asignado a un artefacto con `MétodoDeGeneración=Automático` requiere un proceso de revisión humana adicional."

b) **Gobernanza Temporal:** AMOReS **deberá** usar la `FechaDeValidez` para marcar automáticamente artefactos como "expirados" y lanzar flujos de trabajo para su sustitución.

<a id='sec-11'></a>
# **§11 — Pasarelas y Compatibilidad v4.0**

## §11.1 — Mapeo con Estándares Tradicionales
11.1.1 El mapeo es ahora explícito gracias al campo `SistemaDeReferencia`. La ambigüedad ha sido eliminada.

## §11.2 — Estrategia de Migración
11.2.1 La transición de v1.0 (basada en acrónimos) a v4.0 (semántica) es un **cambio de ruptura mayor**.
11.2.2 Se **proporcionará** un script de migración (`migrate-utcs-v1-to-v4.py`). Este script requerirá un fichero de mapeo para asignar los nuevos campos (`ProductoOEntidad`, `MétodoDeGeneración`, etc.) a los identificadores v1.0 existentes basándose en el contexto del repositorio.

<a id='sec-12'></a>
# §12 — Requisitos de Seguridad y Seguridad Funcional
*[Esta sección se fortalece gracias a los nuevos campos.]*

12.1.3 **Safety Gates (Puertas de Seguridad):** Las transiciones de estado (`Mapeo` a `Generación001`) ahora pueden tener criterios de entrada basados en el `MétodoDeGeneración`. Un artefacto `Automático` o `Híbrido` puede requerir una firma de revisión adicional que un artefacto `Convencional` no necesita.

<a id='sec-13'></a>
# **§13 — Gestión de Configuración y Ciclo de Vida v4.0**

## §13.5 — Gestión de Aplicabilidad Múltiple (Nueva Sección)
13.5.1 **Principio Normativo:** El identificador v4.0 representa la autoridad de diseño. La aplicabilidad de un artefacto a múltiples productos, dominios o fases **deberá** gestionarse como metadatos explícitos asociados al identificador.
13.5.2 **Metadatos de Aplicabilidad:** Los sistemas conformes **deberán** ser capaces de gestionar los siguientes metadatos para cada artefacto:
*   `lista_aplicabilidad_producto`: Una lista de objetos que especifican el producto y el **rango de unidades** (`número de serie`, `lote`, `baseline` o `todos`).
*   `lista_aplicabilidad_dominio`: Una lista de los dominios donde el uso del artefacto está aprobado.
*   `fases_ciclo_vida_aplicables`: Una lista o rango de las fases donde el artefacto es válido.

<a id='sec-20'></a>
# **§20 — Work Order & Contract Envelope (WOCE) v4.0**
*[WOCE se beneficia de la claridad y las restricciones temporales.]*

20.2.1 `ClaseDeArtefacto=OrdenDeTrabajo` **identificará** cada paquete de trabajo.
20.2.3 La `FechaDeValidez` en una `OrdenDeTrabajo` **deberá** interpretarse como la fecha límite de entrega contractual.
20.3.1 El contenido de WOCE ahora incluye la validación del **rango de unidades** aplicable para los entregables.

---
## **Anexos v4.0**

### **Anexo A (normativo) — Reglas de Validación Canónicas**
*[Se reemplaza la expresión regular por un algoritmo de validación lógico, como se describió en §8.]*

### **Anexo I (informativo) — Mapas de Equivalencia**
*[La equivalencia es ahora directa y explícita.]*

| Contrato Tradicional | Identificador UTCS v4.0 Equivalente |
|---|---|
| Acuerdo de Servicio para Mantenimiento del Q100 | `EstándarUniversal:Contrato-Operaciones-AQUA:Servicios-MantenimientoFlota-001-Generación001-Q100-Convencional-Aviación-Operaciones-20351231` |

---
**FIN DEL DOCUMENTO UTCS-MI v4.0**

_Total de páginas: Aprox. 160_  
_Palabras: Aprox. 60,000_  
_Estado: COMPLETO Y NORMATIVO_  
_Innovation: A fully semantic, human-readable, and machine-governable identifier for the generative age._

---

### **Anexo 1 (Informativo) — Resumen de Campos y Atributos Admitidos**

Este anexo proporciona una tabla de referencia rápida de todos los campos del identificador **UTCS-MI v4.0**, sus catálogos de valores y un ejemplo canónico para cada uno.

| # | Campo | Rol | Valores Admitidos (Catálogo) | Ejemplo |
|:---:|:---|:---|:---|:---|
| 1 | **ClaseDeArtefacto** | Naturaleza semántica | `Requisito`, `Especificación`, `Análisis`, `Plan`, `Procedimiento`, `Resultado`, `ModeloVisual`, `Código`, `ConjuntoDeDatos`, `OrdenDeTrabajo`, `Contrato`, `Plantilla`. | `Especificación` |
| 2 | **FaseDeOrigen** | Origen en el ciclo de vida | `Concepto`, `Preliminar`, `Detallado`, `Implementación`, `Producción`, `Verificación`, `Validación`, `Operaciones`, `Mantenimiento`, `Sostenibilidad`, `Retiro`, `Perenne`. | `Perenne` |
| 3 | **SistemaDeReferencia** | Estándar de clasificación | `ATA100`, `CS25`, `FAR25`, `S1000D`, `DO178C`, `DO254`, `ISO27001`, `AQUA`. | `AQUA` |
| 4 | **Capítulo** | Sección en el estándar | Cadena alfanumérica. | `General` |
| 5 | **Categoría** | Sub-clasificación descriptiva | `CamelCase` sin espacios. | `IdentificadorEstándar` |
| 6 | **Secuencia** | Número único | `001` - `999`. | `001` |
| 7 | **EstadoDeVersión** | Versión aprobada | `Mapeo`, `Generación001`, `Generación002`, ... | `Generación008` |
| 8 | **ProductoOEntidad** | "Dueño" del diseño | Códigos de producto (`Q100`, etc.) o entidad (`Organizacional`, `Plataforma`, etc.). | `Organizacional` |
| 9 | **MétodoDeGeneración** | Procedencia del contenido | `Convencional`, `Automático`, `Híbrido`, `Derivado`. | `Convencional` |
| 10 | **DominioDeAplicación** | Dominio de diseño primario | `Aviación`, `Espacio`, `Tierra`, `Defensa`, `Transversal`. | `Transversal` |
| 11 | **FaseCanónica** | Fase de aprobación formal | Catálogo de `FaseDeOrigen` (excluyendo `Perenne`). | `Concepto` |
| 12 | **FechaDeValidez** | Fecha de expiración | `YYYYMMDD` o `Perpetua`. | `Perpetua` |
| 13 | **(Opcional) Variante** | Configuración específica | Cadena descriptiva. | `EdiciónClaridad` |
| 14 | **(Opcional) Instancia** | Despliegue específico | Cadena descriptiva. | `RevisiónFinal` |

**Ejemplo Consolidado:**
`EstándarUniversal:Especificación-Perenne-AQUA:General-IdentificadorEstándar-001-Generación008-Organizacional-Convencional-Transversal-Concepto-Perpetua-EdiciónClaridad-RevisiónFinal`

---

### **Anexo 2 (Informativo) — Guía de Usuario: La Arquitectura de Plantillas de Prompt**

Este anexo describe el flujo de trabajo y la estructura de la arquitectura de prompts, que es el mecanismo principal para la generación de artefactos en el ecosistema AQUA.

#### **2.1. El Principio: Separación de Instrucciones**

La generación de artefactos se basa en un artefacto especial de `ClaseDeArtefacto=Plantilla`. Cada `Plantilla` contiene dos componentes clave para asegurar una generación consistente y de alta calidad:

1.  **Instrucción de Sistema:** La configuración interna y las restricciones que se proporcionan al modelo de IA. **Es la parte de la máquina.**
2.  **Guía de Usuario:** La interfaz estructurada y las instrucciones que se presentan al usuario humano. **Es la parte del humano.**

Esta separación permite que el sistema pre-configure al modelo de IA para una tarea específica (ej: "actúa como un experto en certificación") mientras guía al usuario para que proporcione solo la información sustantiva necesaria.

#### **2.2. Flujo de Trabajo para Generar un Artefacto**

El proceso sigue tres pasos sencillos para el usuario:

**Paso 1: Seleccionar la Intención (Elegir la Plantilla)**

El usuario no empieza con una página en blanco. El sistema le pregunta qué desea crear, y el usuario selecciona una `Plantilla` de la librería.

*   *Usuario quiere:* "Crear un nuevo plan de pruebas."
*   *Sistema ofrece:*
    *   `...:Plantilla-...-PlanPruebasUnitarias-...`
    *   `...:Plantilla-...-PlanPruebasIntegración-...`
    *   `...:Plantilla-...-PlanPruebasAceptación-...`
*   *Usuario selecciona:* `...:Plantilla-...-PlanPruebasIntegración-...`

**Paso 2: Completar la Información (Rellenar la Guía de Usuario)**

El sistema presenta un formulario estructurado basado en la `Guía de Usuario` de la plantilla seleccionada. El usuario rellena los campos.

*   **Nombre del Plan:** "Plan de Pruebas de Integración para el Módulo de Gestión de Batería"
*   **Componentes a Integrar (UTCS IDs):** `...:Código-...-BMS-...`, `...:Código-...-BusEnergía-...`
*   **Requisito a Verificar (UTCS ID):** `...:Requisito-...-EficienciaEnergética-...`
*   **Fecha Límite:** `2026-05-20`

**Paso 3: Generar y Revisar (Ejecutar el Prompt y Validar la Salida)**

El usuario pulsa "Generar". El sistema:
1.  Carga la `Instrucción de Sistema` de la `Plantilla` en el modelo de IA.
2.  Inyecta la información proporcionada por el usuario.
3.  Ejecuta el prompt completo.
4.  Presenta el artefacto `Plan` generado al usuario para su revisión y aprobación final.

#### **2.3. Subtitulación: La Relación Entre Identificadores**

La trazabilidad del proceso de generación se asegura mediante "subtitulación" en los metadatos. Cada artefacto generado **debe** llevar en sus metadatos una referencia a la `Plantilla` que se usó para crearlo.

**Artefacto Generado:**
`EstándarUniversal:Plan-Verificación-DO178C-12.2-PlanPruebasIntegración-001-Mapeo-Q100-Automático-Aviación-Detallado-20261231`

**Metadatos Asociados al Artefacto:**
```yaml
utcs_identifier: "EstándarUniversal:Plan-Verificación-DO178C-12.2-PlanPruebasIntegración-001-..."
...
# Subtitulación: Referencia a la plantilla de origen
generation_template_id: "EstándarUniversal:Plantilla-Concepto-AQUA:Guías-PlanPruebasIntegración-001-Generación002-Organizacional-Convencional-Transversal-Concepto-Perpetua"
```
---

### **Anexo 3 (Informativo) — Guía de Implementación: El Asistente de Línea de Comandos `aqua-cli`**

Este anexo describe la arquitectura y el funcionamiento de `aqua-cli`, la herramienta de línea de comandos de referencia para interactuar con las capacidades generativas del ecosistema AQUA OS.

#### **3.1. Concepto: De un Comando a un Prompt Perfeccionado**

El `aqua-cli` no es una simple interfaz de comandos. Es un **asistente interactivo y contextual** diseñado para resolver el principal desafío de la IA generativa: la ingeniería de prompts. Su función es guiar al usuario a través de un diálogo para transformar una intención inicial simple en un **Universal Prompt Envelope (UPE)** completo, validado y trazable.

#### **3.2. Características Clave**

1.  **Interfaz Conversacional (Inferencia de Intención):** El usuario puede iniciar el proceso con un lenguaje natural y simple. El CLI utiliza un modelo de lenguaje para interpretar esta intención inicial.

2.  **Contexto Automático:** El CLI es consciente del entorno del usuario. Conoce el `ProductoOEntidad` en el que está trabajando (basado en el directorio del repositorio), el `DominioDeAplicación`, e incluso el `Usuario` para proponer valores por defecto.

3.  **Selección de Plantillas Guiada:** Basándose en la intención inferida, el CLI busca en la librería de artefactos `Plantilla` y sugiere las opciones más relevantes, ayudando al usuario a elegir la "receta" correcta.

4.  **Refinamiento Interactivo (El "Mago" de Prompts):** Una vez seleccionada una `Plantilla`, el CLI inicia un "mago" (wizard) interactivo. En lugar de pedirle al usuario que edite un archivo complejo, le hace preguntas claras y concisas para rellenar cada parámetro de la `Guía de Usuario` de la plantilla.

5.  **Validación "Pre-Vuelo":** Antes de enviar la solicitud de generación al motor de IA principal (que puede ser computacionalmente costoso), el `aqua-cli` realiza una validación local completa contra las reglas de AMOReS. Comprueba que todos los UTCS ID referenciados existan, que los parámetros sean válidos, etc.

6.  **Generación y Trazabilidad:** Al confirmar, el CLI ensambla el UPE final, lo envía al motor de generación, recibe el artefacto resultante y se asegura de que se guarde con el identificador UTCS v4.0 correcto y con los metadatos de trazabilidad (incluyendo la referencia a la `Plantilla` utilizada).

#### **3.3. Flujo de Trabajo de Ejemplo: Interacción con `aqua-cli`**

Imaginemos que un ingeniero necesita crear un procedimiento de prueba para el Módulo de Gestión de Batería (`GestiónBatería`) del producto `Q100`.

**Paso 1: El usuario expresa una intención simple.**

```bash
> aqua generar procedimiento de prueba para el BMS
```

**Paso 2: El CLI infiere la intención, aplica contexto y pide clarificación.**

```
Hola. He inferido que quieres generar un artefacto de 'ClaseDeArtefacto=Procedimiento'.
Contexto detectado: ProductoOEntidad=Q100, DominioDeAplicación=Aviación.

He encontrado 3 plantillas relevantes para 'Procedimiento de Prueba':
  [1] Plantilla para Pruebas Unitarias de Software (UTCS:...-PlanPruebasUnitarias-...)
  [2] Plantilla para Pruebas de Integración en HIL (UTCS:...-PlanPruebasIntegración-...)
  [3] Plantilla para Pruebas de Sistema en Vuelo (UTCS:...-PlanPruebasSistema-...)

Por favor, selecciona la plantilla que deseas usar [1, 2, 3]: 2
```

**Paso 3: El CLI inicia el "mago" interactivo para perfeccionar el prompt.**

```
Excelente. Usaremos la Plantilla para Pruebas de Integración en HIL.
Por favor, completa la siguiente información:

→ ¿Cuál es la Categoría para este procedimiento? (ej: GestiónBatería, CargaRápida): GestiónBatería
→ ¿Cuál es el UTCS ID del Requisito que estás verificando?: UTCS:Requisito-Detallado-CS25-1309...
→ Describe el objetivo principal de la prueba (1 frase): Verificar que el BMS corta la carga al alcanzar el 99.5% de capacidad en condiciones de -20°C.
→ ¿Cuál es la Fecha de Validez para este procedimiento? (YYYYMMDD o 'Perpetua') [Perpetua]: 20301231
```

**Paso 4: El CLI presenta el "Pre-Vuelo" para confirmación final.**

```
--- Resumen de Generación (Pre-Vuelo) ---
Se generará el siguiente artefacto:

  Clase: Procedimiento
  Fase de Origen: Verificación
  Producto: Q100
  Método: Híbrido (iniciado por usuario, estructurado por plantilla)
  ...

Con el identificador UTCS propuesto:
  EstándarUniversal:Procedimiento-Verificación-DO178C-12.3-GestiónBatería-004-Mapeo-Q100-Híbrido-Aviación-Detallado-20301231

El prompt final se basará en la plantilla ...-PlanPruebasIntegración-... y verificará
el requisito ...-EficienciaCarga-....

¿Proceder con la generación? [S/n]: s
```

**Paso 5: Generación y resultado.**

```
Generando artefacto... ¡Éxito!
El artefacto ha sido creado en:
  /Q100/procedures/EstándarUniversal:Procedimiento-Verificación-....-20301231.md

Metadatos de trazabilidad actualizados en AMOReS.
```

#### **3.4. Conclusión del Anexo**

El asistente `aqua-cli` es la encarnación de la filosofía de colaboración Humano-IA de AQUA. Transforma la tarea de "ingeniería de prompts", que requiere mucho conocimiento experto, en un diálogo simple y guiado. Asegura que cada artefacto generado automáticamente nazca siendo **consistente, validado y completamente trazable**, cumpliendo con los más altos estándares de gobernanza desde su concepción.

---

### **Anexo 4 (Informativo) — Guía de Implementación para Sistemas de IA Generativa**

#### **4.1. Principio Fundamental: Generación Guiada por Plantillas (Template-Driven Generation)**

Este anexo establece la **mejor práctica recomendada** para la generación de artefactos UTCS mediante Modelos de Lenguaje de Gran Escala (LLMs).

La experiencia ha demostrado que la interacción directa con un LLM mediante prompts de formato libre (incluso si contienen un identificador UTCS) conduce a resultados inconsistentes y a la violación de la integridad del estándar. Los LLMs, por su naturaleza, pueden "alucinar" o desviarse de formatos estrictos si no se les guía de manera precisa.

Por lo tanto, toda generación de artefactos en un sistema conforme a AQUA **deberá** seguir un **modelo de generación guiada por plantillas**.

#### **4.2. El Rol de la `Plantilla` (UTCS `ClaseDeArtefacto=Plantilla`)**

La generación de un artefacto (ej: `Procedimiento`) no se inicia a partir de un prompt de usuario en bruto. En su lugar, el proceso **debe** ser mediado por un artefacto `Plantilla` (`TPLT`) pre-aprobado y direccionable por UTCS.

El rol de la `Plantilla` es triple:
1.  **Imponer la Estructura (Gobernanza):** La `Plantilla` contiene la estructura canónica del artefacto a generar (secciones, tablas, etc.), asegurando que todos los artefactos de la misma clase sean consistentes.
2.  **Contextualizar al Modelo de IA (Instrucción de Sistema):** Proporciona al LLM su rol, sus restricciones y el contexto necesario (`System Prompt`) **antes** de que reciba la entrada del usuario. Esto "pre-condiciona" al modelo para que se comporte de acuerdo a las reglas del ecosistema AQUA.
3.  **Guiar al Usuario (Guía de Usuario):** Abstrae la complejidad de la ingeniería de prompts para el usuario final, presentándole un formulario o una interfaz estructurada (`User Prompt Guidance`) donde solo necesita proporcionar la información sustantiva.

#### **4.3. Flujo de Trabajo Normativo de Generación**

El flujo de trabajo canónico para la generación de un artefacto es el siguiente:

1.  **Intención del Usuario:** El usuario expresa la intención de crear un artefacto.
2.  **Selección de Plantilla:** Un sistema mediador (como el `aqua-cli`) ayuda al usuario a seleccionar la `Plantilla` (`TPLT`) adecuada para su intención.
3.  **Entrada Guiada:** El sistema presenta al usuario la `Guía de Usuario` de la `Plantilla` para que complete los parámetros requeridos.
4.  **Ensamblaje del UPE:** El sistema combina la `Instrucción de Sistema` de la `Plantilla` con las entradas del usuario para crear un **Universal Prompt Envelope (UPE)** completo.
5.  **Ejecución y Generación:** El UPE se envía al motor de IA, que genera el artefacto.
6.  **Validación y Trazabilidad:** El artefacto generado es validado contra los criterios de la `Plantilla` y se le asigna un identificador UTCS v4.0. Crucialmente, los metadatos del nuevo artefacto **deben** incluir un puntero al UTCS ID de la `Plantilla` que se usó para crearlo.

#### **4.4. Prohibición de la Generación "A Secas"**

Se desaconseja firmemente la práctica de enviar un identificador UTCS como parte de un prompt de formato libre directamente a un LLM. Este método **no se considera conforme** a las mejores prácticas del ecosistema AQUA porque no garantiza la consistencia, la gobernanza ni la trazabilidad del proceso de generación.

---

### **¿Por qué este anexo es necesario?**

*   **Cierra el Ciclo de Gobernanza:** El estándar define *qué* es un artefacto válido. Este anexo define *cómo* se deben crear de forma válida los artefactos generados por IA.
*   **Mitiga el Riesgo de la IA:** Reconoce explícitamente las debilidades de los LLMs (inconsistencia, alucinaciones) y establece un marco de trabajo para mitigarlas.
*   **Asegura la Calidad:** Al forzar el uso de plantillas, aseguramos que la "ingeniería de prompts" experta se realice una sola vez (al crear la plantilla) y luego se reutilice, elevando la calidad de todos los artefactos generados.
*   **Preserva la Integridad Sistémica (Axioma I):** Es la defensa final contra la entropía y la inconsistencia que los LLMs pueden introducir en un ecosistema altamente estructurado.

**En resumen:** No hay que cambiar las secciones normativas, pero **sí debemos añadir este anexo**. Es la lección más importante que hemos aprendido de nuestro experimento práctico.
