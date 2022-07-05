import re


def get_nvidia_model(description):
    if 'radeon' not in description and 'amd' not in description:
        model = re.search('(gtx|rtx|gt|gv|p|g|a)((\s\d{4}|\d{4})|(\s\d{3}|\d{3}))', description)
        return model.group() if model else None


def get_radeon_model(description):
    if 'nvidia' not in description and 'geforce' not in description:
        model = re.search('((r([1-9]|x)(\s\d+|\d+))|(w([1-9]|x)(\s\d+|\d+))|hd(\s\d+|\d+))(xt|\sxt|\d)',
                          description)
        return model.group() if model else None


def get_lhr(description):
    return 'lhr' if 'lhr' in description else ''


def get_super(description):
    return 'super' if 'super' in description else ''


def get_oc(description):
    return 'oc' if 'oc' in description else ''


def get_ti(description):
    return 'ti' if 'ti' in description else ''


def get_memory_size(description):
    memory_size = re.sub('([1-9]\d gbps)|([1-9]\dgbps)', '', description)
    memory_size = re.search('[1-9]\dgb|[1-9]\d gb|[1-9]\dg|[1-9]gb|[1-9] gb|[1-9]g', memory_size)
    if memory_size:
        memory_size = memory_size.group()+'b' if memory_size.group().endswith('g') else memory_size.group()
        # separates alphabetic and number
        memory_size = re.sub(r'([0-9]+(\.[0-9]+)?)', r' \1 ', memory_size)
        memory_size = re.sub(' +', ' ', memory_size)
    else:
        memory_size = ''

    return memory_size.upper()


def get_memory_type(description):
    memory_type = re.search('gddr\d|ddr\d', description)
    return memory_type.group().upper() if memory_type else ''


def get_brand(description):
    brands = [
        'asus', 'evga', 'galax', 'gigabyte', 'msi', 'pny', 'zotac',
        'afox', 'asrock', 'barrow', 'duex', 'imperiums', 'pcyes',
        'power color', 'powercolor', 'sapphire', 'xfx', 'bluecase',
        'colorful', 'gainward', 'hp', 'palit', 'biostar', 'inno3d',
        'superframe', 'leadtek', 'mancer', 'enzatec', 'zogis', 'radeon pro', 'igame'
    ]

    for brand in brands:
        if brand in description:
            return brand.replace('powercolor', 'power color').upper()

    return ''


def builds_manufacturers(model):
    return 'RADEON' if re.search('^W.|^RX.|^R\d.|^HD.', model) else 'NVIDIA'


def builds_title(brand, model, var_super, ti, overclock, lhr, memory_size, manufacturer):
    title = f'{brand} {manufacturer} {model} {var_super} {ti} {overclock} {lhr} {memory_size}'.upper()
    return re.sub(' +', ' ', title)


def builds_model(description):
    model = ''
    description = re.sub('(\d{3}|\d{2})(\s|.)bit(\s|s)', '', description)
    nvidia_model = get_nvidia_model(description)
    radeon_model = get_radeon_model(description)

    if nvidia_model:
        model = nvidia_model
        # separates the model name from the model number
        # example: gtx3070 to gtx 3070
        if not re.search('\At[1-9]([0-9]{3}|[0-9]{2})', description):
            model = re.sub(r'([0-9]+(\.[0-9]+)?)', r' \1 ', model)

    elif radeon_model:
        model = radeon_model
        # separates the model name from the model number
        # example: rx6500 to rx 6500 |r5230 to r5 230
        if re.search('^rx|^w', model):
            model = re.sub(r'([0-9]+(\.[0-9]+)?)', r' \1 ', model)

        # example: r5230 to r5 230
        elif re.search('^r[1-9]', model):
            model = re.sub(r'(r\d)(\d{1,2})', r'\1 \2', model)

    return re.sub(' +', ' ', model).upper()


def creates_data_dict(index, worksheet):
    description = str(worksheet[f'A{index}'].value).lower()
    description = re.sub(r'[^a-zA-Z0-9]+', ' ', description)

    link = worksheet[f'B{index}'].value
    store = worksheet[f'C{index}'].value
    price = 'R$'+worksheet[f'D{index}'].value
    brand = get_brand(description)
    memory_type = get_memory_type(description)
    memory_size = get_memory_size(description)
    lhr = get_lhr(description)
    ti = get_ti(description)
    var_super = get_super(description)
    overclock = get_oc(description)
    model = builds_model(description)
    manufacturer = builds_manufacturers(model)
    title = builds_title(brand, model, var_super, ti, overclock, lhr, memory_size, manufacturer)

    check = 'X'
    rtx, gtx, rx, gt, lhr, ti, var_super, oc = (
        'RTX', 'GTX', 'RX', 'GT', 'LHR', 'TI', 'SUPER', 'OC')

    rtx = check if rtx in title else ''
    gtx = check if gtx in title else ''
    rx = check if rx in title else ''
    gt = check if gt in title else ''
    lhr = check if lhr in title else ''
    ti = check if ti in title else ''
    var_super = check if var_super in title else ''
    oc = check if oc in title else ''

    return {
        'link': link, 'price': price, 'store': store,
        'manufacturers': manufacturer, 'brand': brand,
        'memory_size': memory_size, 'model': model,
        'memory_type': memory_type, 'lhr': lhr,
        'oc': oc, 'ti': ti, 'super': var_super, 'title': title,
        'rtx': rtx, 'gtx': gtx, 'rx': rx, 'gt': gt,
    }
