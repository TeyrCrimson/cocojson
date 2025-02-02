import cv2

from .common import get_ltrbwh

BUFFER=2

def draw_annot(img, annot, color=(255,255,0), thickness=1, font=cv2.FONT_HERSHEY_DUPLEX, fontScale=1.0):
    ltrb = get_ltrbwh(annot['bbox'])[:4]
    draw_bb(img, ltrb, color=color, thickness=thickness)
    draw_text(img, ltrb, annot, font=font, fontScale=fontScale, color=color, thickness=thickness)
    
def draw_bb(img, ltrb, color=(255,255,0), thickness=1):
    l,t,r,b = ltrb
    cv2.rectangle(img, (l,t), (r,b), color=color, thickness=thickness)

def draw_text(img, ltrb, annot, font=cv2.FONT_HERSHEY_DUPLEX, fontScale=1.0, color=(255,255,0), thickness=1.0):
    l,t,r,b = ltrb
    cat_id = annot['category_id']
    try:
        occluded = annot['attributes']['occluded']
    except KeyError:
        occluded = None
    try:
        iscrowd = annot['iscrowd']
    except KeyError:
        iscrowd = None
    try:
        ignore = annot['ignore']
    except KeyError:
        ignore = None
    try:
        tid = annot['attributes']['track_id']
    except KeyError:
        tid = None

    text = f"{cat_id}"
    if tid is not None:
        text += f';t{tid}'
    if occluded:
        text += ';oc'
    if iscrowd:
        text += ';cr'
    if ignore:
        text += ';ig'
    text_size, _ = cv2.getTextSize(text, font, fontScale, thickness)
    _, text_h = text_size
    cv2.putText(img, 
            text, 
            (l+BUFFER, t+text_h+(BUFFER+2)), 
            fontFace=font, fontScale=fontScale, color=color, thickness=thickness)
