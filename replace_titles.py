# Replace or create titles, using h1
#
# Mike McCaffrey
# mjmccaffrey@gmail.com
# June 2018


import os
import re
import sys


def files_to_process(processing_root):
    #
    for root, dirs, files in os.walk(processing_root):
        for file in files:
            if file.lower().endswith('.htm'):
                yield os.path.join(root, file)
                

def h1_text(content):
    #
    h1 = re.search(
                pattern='<h1.*?>(.*?)</h1>',
                string=content,
                flags=re.IGNORECASE | re.DOTALL,
                )
    if h1 is None:
        return None
    result = re.sub(
            pattern='<(a|MadCap|img|sub|/).*?>', 
            repl='', 
            string=h1.group(1), 
            ).strip()
    return result

    
def title_start_end_text(content):
    #    
    title = re.search(
                pattern='<title.*?>(.*?)</title>',
                string=content,
                flags=re.IGNORECASE | re.DOTALL
                )
    if title is None:
        return None, None, None
    return title.start(1), title.end(1), title.group(1).strip()

    
def head_start(content):
    #    
    head = re.search(
                pattern='<head.*?>(.*?)</head>',
                string=content,
                flags=re.IGNORECASE | re.DOTALL
                )
    if head is None:
        return None
    return head.start(1)


def replace_title(content):
    #
    h1 = h1_text(content)
    if h1 is None:
        log.write('H1 NOT FOUND! SKIPPING.\n')
        return None
    log.write('{},'.format(h1))
    
    t_start, t_end, t_text = title_start_end_text(content)
    if t_text is None:
        h_start = head_start(content)
        if h_start is None:
            log.write('TITLE AND HEAD NOT FOUND! SKIPPING.\n')
            return None
        log.write('TITLE NOT FOUND. CREATING.\n')
        return (
            content[:h_start] + 
            '\n        ' + 
            '<title>{}</title>'.format(h1) + 
            content[h_start:]
            )
    log.write('{}\n'.format(t_text))
    return (
        content[:t_start] + 
        h1 + 
        content[t_end:]
        )

    
def process_file(path):
    #
    log.write('{},'.format(path))
    
    with open(
            file=path, 
            mode='r', 
            encoding='utf-8',
            errors='surrogateescape',
            ) as f:
        text_in = f.read()
        
    text_out = replace_title(text_in)
    if text_out is None:
        return
        
    with open(
            file=path, 
            mode='w', 
            encoding='utf-8', 
            errors='surrogateescape', 
            ) as f:
        f.write(text_out)

        
def main():        
    #
    global log
    
    with open(
            file='replace_titles.log', 
            mode='w',
            ) as log:
        log.write('FILE,FIRST_H1,OLD_TITLE\n')  
        for file in files_to_process(sys.argv[1]):
            process_file(file)

            
if __name__ == "__main__":
    main()
