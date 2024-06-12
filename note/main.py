import note.loader, note.dumper, sys

# format >notes compile raw bin


note.dumper.dump_document(note.loader.parse_notes("test/raw")[0], "test/build")
