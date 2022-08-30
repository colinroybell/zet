from jinja2 import Template, Undefined
JINJA2_ENVIRONMENT_OPTIONS = { 'undefined' : Undefined }

import docutils
from docutils.core import publish_parts
import os

root_in = "/mnt/c/Users/colin/Dropbox/Zet/"
root_out = "/mnt/c/Users/colin/Dropbox/Zout/"

def process_dir(dir):
    print(f'Processing dir {dir}')
    files = os.scandir(root_in+dir)
    for file in files:
        print(f'Found {file.name} in {dir}')
        if file.is_dir():
            process_dir(dir+file.name+'/')
        else:
            process_file(dir,file.name)   

def process_function(extension):
    processes = {'.rst': process_rst, '.txt': process_txt}
    if extension in processes:
        return processes[extension]
    else:
        return None    

def process_rst(filename):
    with open(filename,'r') as f:
        file = f.read()

        t = Template(file)
        
        # Hack to keep test working 
        inserted_text = {"one": "one", "two": "tw**o**"}

        rendered = t.render(inserted_text = inserted_text)
        
        html = docutils.core.publish_string(source=rendered,writer_name="html",settings_overrides={'output_encoding':'unicode'})
        return html

def process_txt(filename):
    with open(filename,'r') as f:
        file = f.readlines()
        lines = ['::','']
        lines.extend(['  '+line.rstrip() for line in file])
        print(lines)
        text = '\n'.join(lines)
        t = Template(text)
        rendered = t.render()
        
        html = docutils.core.publish_string(source=rendered,writer_name="html",settings_overrides={'output_encoding':'unicode'})
        return html

def process_file(dir, filename):
    print(f'Processing {root_in+dir+filename}')
    
    dir_out = root_out + dir
    base, extension = os.path.splitext(filename)
    fn = process_function(extension)

    if fn:
        output = fn(root_in+dir+filename)
        
        filename_out = base+".html"
        if not os.path.exists(dir_out):
            os.makedirs(dir_out) 
        print(f'Writing {dir_out+filename_out}')    
        with open(dir_out+filename_out,'w') as f:
            f.write(output) 
  
process_dir('')

  
