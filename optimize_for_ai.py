import sys
from pathlib import Path
from docx import Document
from markitdown import MarkItDown

def clean_docx(input_path: Path, temp_clean_path: Path):
    """
    Carga el archivo .docx y elimina encabezados y pies de página repetitivos 
    que consumen tokens innecesarios en la IA.
    """
    doc = Document(input_path)
    
    # Eliminar encabezados y pies de página de todas las secciones
    for section in doc.sections:
        section.header.is_linked_to_previous = False
        section.footer.is_linked_to_previous = False
        
        # Limpiar texto de los encabezados
        for p in section.header.paragraphs:
            p.text = ""
        # Limpiar texto de los pies de página
        for p in section.footer.paragraphs:
            p.text = ""

    doc.save(temp_clean_path)

def convert_to_ai_formats(input_file: str):
    file_path = Path(input_file).expanduser().resolve()

    # Si no existe en la carpeta actual, buscar en ~/Documents y ~/Downloads
    if not file_path.exists():
        search_dirs = [Path.home() / "Documents", Path.home() / "Downloads"]
        found = False
        for folder in search_dirs:
            candidate = folder / input_file
            if candidate.exists():
                file_path = candidate
                found = True
                break
        
        if not found:
            print(f"Error: No se encontró '{input_file}' en el directorio actual, ni en Documents ni en Downloads.")
            return

    print(f"Procesando: {file_path}")
    print("Limpiando el documento...")
    temp_clean_path = file_path.parent / f"temp_{file_path.name}"
    clean_docx(file_path, temp_clean_path)

    print("Convirtiendo a formatos para IA...")
    md = MarkItDown()
    result = md.convert(str(temp_clean_path))
    
    output_md = file_path.with_suffix('.md')
    with open(output_md, 'w', encoding='utf-8') as f:
        f.write(result.text_content)

    output_txt = file_path.with_suffix('.txt')
    with open(output_txt, 'w', encoding='utf-8') as f:
        f.write(result.text_content)

    if temp_clean_path.exists():
        temp_clean_path.unlink()

    print(f"\n¡Listo! Archivos generados en {file_path.parent}:")
    print(f" - {output_md.name}")
    print(f" - {output_txt.name}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Uso: python optimize_for_ai.py mi_documento.docx")
    else:
        convert_to_ai_formats(sys.argv[1])
