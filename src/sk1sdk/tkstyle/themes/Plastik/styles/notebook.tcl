style element create Notebook.client image "notebook-c" -border 4
style element create Notebook.tab image [list "notebook_tn" \
   selected   "notebook_ts" \
   active     "notebook_ta" \
   ] -padding {0 2 0 0} -border {4 10 4 10}

style configure TNotebook -tabmargins {2 2 0 0}
style configure TNotebook.Tab -padding {6 2 6 2} -expand {0 0 2}
style map TNotebook.Tab -expand [list selected {1 2 4 2}]
