# Overview

Tepkit creates a series of classes for handling different types of files from different sources.

## Basic Classes

```{mermaid}
graph TB;
    File --> TextFile;
    TextFile --> StructuredTextFile;
    TextFile --> TableTextFile;
```

- `File`: The base class for all files, providing basic `.from_file()` and `.from_dir()` methods.
- `TextFile`: The base class for text files,
  which is divided into two categories:
  `StructuredTextFile` and `TableTextFile`.
  - `StructuredTextFile`: A class for handling structured text files.  
  Used for text files that do not store data in tabular form but follow a specific structured format.
  - `TableTextFile`: A class for handling tabular text files.  
  Used for files where the main data can be parsed as a table.
  - The tabular data will be parsed into a pandas DataFrame and stored in `self.df`.
  - (Tentative) The other non-tabular data will be stored in `self.data`.
  - (Tentative) The additional data will be stored in `self.extra_data`.

## Classes for Various Software

- [VASP File Classes](vasp_file_classes)
- [BoltzTraP2 File Classes](boltztrap2_file_classes)
- [Phonopy File Classes](phonopy_file_classes)
- [ShengBTE File Classes](shengbte_file_classes)

