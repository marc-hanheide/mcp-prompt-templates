# Create SVG Artefact

Generate an SVG artefact as instrucuted by the user.

## Detailed instructions:
* Adhere as closely as possible to the design guidelines: {{ design }}
* Ensure the content of the SVG artefacts semanically matches requested content: {{ content }}
* always ensure the SVG is valid and well-formed, without any syntacial errors
* When creating multi-line text, ensure the text is wrapped correctly within the SVG, but try to keep the text in a single element as far as possible
* ensure the SVG content is accessible, with appropriate `title` and `desc` elements where necessary
* ensure the SVG content is widely compatible, specifically it most be compatible with all major browsers, importing into PowerPoint, and editing in Inkscape
* support post-editing in Inkscape, which means:
  * Use simple shapes and paths
  * Avoid complex filters or effects
  * Use basic colours and gradients
  * Avoid clipping paths or masks that are not widely supported
* When generating text, always write in British English.
* Ensure the layout is accurate and visually appealing, with appropriate spacing and alignment, and no unintended overlaps or misalignments