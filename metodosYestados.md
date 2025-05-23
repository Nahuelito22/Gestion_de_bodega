# Entidades y métodos

---

## 1. VariedadUva

* GET /variedades: obtener todas
* GET /variedades/{id}: obtener una
* POST: crear una nueva variedad
* PUT: reemplazar
* PATCH: modificar algo puntual (opcional)
* DELETE: eliminar variedad (opcional si no está usada)

📌 Si una variedad está asociada a un lote, no deberías permitir borrarla.

---

## 2. LoteVino

Es central y debe ser trazable. No deberías eliminarlo nunca.

* GET /lotes: ver todos los lotes
* GET /lotes/{id}: ver detalle completo de un lote
* POST: crear nuevo lote
* PATCH: actualizar comentarios, por ejemplo
* DELETE: ❌ No recomendable (mejor usar "estado inactivo" si hace falta)

---

## 3. RecepcionUva

Es parte del flujo, se crea una vez por lote.

* GET /recepcion: listar todas
* GET /recepcion/{id}: ver una
* POST: registrar nueva recepción de uva
* PATCH: ajustar peso, pH, etc. si hubo error de carga
* DELETE: ❌ No recomendable (perdés trazabilidad)

---

## 4. FermentacionAlcoolica

Una sola por lote (generalmente). Parte del flujo técnico.

* GET /fermentacion: todas
* GET /fermentacion/{id}
* POST: registrar inicio/fin de fermentación
* PATCH: corregir temperaturas, datos químicos
* DELETE: ❌ No, es histórica

---

## 5. CrianzaAlmacenamiento

Puede haber múltiples por lote (si se trasiega). Importante para seguimiento.

* GET /crianza: todas
* GET /crianza/{id}
* POST: registrar nueva crianza
* PATCH: ajustar duración, recipiente
* DELETE: ❌ No recomendable

---

## 6. Embotellado

Última etapa. Podría haber más de uno por lote (ej: en tandas).

* GET /embotellado
* GET /embotellado/{id}
* POST: registrar embotellado
* PATCH: ajustar cantidad o alcohol si se cargó mal
* DELETE: ❌ No debería eliminarse

---


## 📌 Resumen visual

| Entidad               | GET | POST | PUT | PATCH | DELETE | Notas clave                              |
| --------------------- | --- | ---- | --- | ----- | ------ | ---------------------------------------- |
| VariedadUva           | ✅   | ✅    | ✅   | ✅     | ⚠️     | Solo borrar si no está usada             |
| LoteVino              | ✅   | ✅    | ❌   | ✅     | ❌      | Nunca eliminar por trazabilidad          |
| RecepcionUva          | ✅   | ✅    | ❌   | ✅     | ❌      | Parte inicial del proceso, no se elimina |
| FermentacionAlcoolica | ✅   | ✅    | ❌   | ✅     | ❌      | Técnica y trazable, histórica            |
| CrianzaAlmacenamiento | ✅   | ✅    | ❌   | ✅     | ❌      | Puede haber varias etapas, no se elimina |
| Embotellado           | ✅   | ✅    | ❌   | ✅     | ❌      | Última etapa, no debería borrarse        |



---


## 📦 Entidades y sus estados

| Entidad          | ¿Usar estado? | Ejemplo de estados                         |
| ---------------- | ------------- | ------------------------------------------ |
| **VariedadUva**  | Opcional      | `activo`, `inactivo` (si ya no se usa más) |
| **LoteVino**     | ✅ Obligatorio | `activo`, `finalizado`, `en_proceso`, etc. |
| **RecepcionUva** | Opcional      | `validada`, `pendiente`, `anulada`         |
| **Fermentacion** | ✅ Recomendado | `en_proceso`, `completada`, `cancelada`    |
| **Crianza**      | ✅ Recomendado | `en_barrica`, `trasvasado`, `terminado`    |
| **Embotellado**  | ✅ Recomendado | `programado`, `completado`, `fallido`      |

