import re
import csv

def parse_obo_file(file_path):
    main_uberon_with_children = []
    main_uberon_with_mesh_umls = []

    current_term = {}
    current_is_a = []
    current_xrefs = []

    with open(file_path, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if line.startswith('[Term]'):
                if current_term:
                    if current_is_a:
                        main_uberon_with_children.append({
                            'main_uberon_id': current_term['id'],
                            'children': current_is_a
                        })
                    if current_xrefs:
                        mesh_ids = []
                        umls_ids = []
                        for xref in current_xrefs:
                            if xref.startswith('MESH:'):
                                mesh_ids.append(xref.split('MESH:')[1])
                            elif xref.startswith('UMLS:'):
                                umls_ids.append(xref.split('UMLS:')[1])
                        if mesh_ids or umls_ids:
                            main_uberon_with_mesh_umls.append({
                                'main_uberon_id': current_term['id'],
                                'mesh_ids': ','.join(mesh_ids),
                                'umls_ids': ','.join(umls_ids)
                            })
                    current_term = {}
                    current_is_a = []
                    current_xrefs = []
            elif line.startswith('[Typedef]'):
                continue
            elif line.startswith('id: '):
                current_term['id'] = line.split('id: ')[1]
            elif line.startswith('is_a: '):
                is_a_id = line.split('is_a: ')[1].split(' ! ')[0]
                current_is_a.append(is_a_id)
            elif line.startswith('xref: '):
                xref_id = line.split('xref: ')[1]
                current_xrefs.append(xref_id)

    if current_term:
        if current_is_a:
            main_uberon_with_children.append({
                'main_uberon_id': current_term['id'],
                'children': current_is_a
            })
        if current_xrefs:
            mesh_ids = []
            umls_ids = []
            for xref in current_xrefs:
                if xref.startswith('MESH:'):
                    mesh_ids.append(xref.split('MESH:')[1])
                elif xref.startswith('UMLS:'):
                    umls_ids.append(xref.split('UMLS:')[1])
            if mesh_ids or umls_ids:
                main_uberon_with_mesh_umls.append({
                    'main_uberon_id': current_term['id'],
                    'mesh_ids': ','.join(mesh_ids),
                    'umls_ids': ','.join(umls_ids)
                })

    return main_uberon_with_children, main_uberon_with_mesh_umls

def write_to_csv(data, filename, fieldnames):
    with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for item in data:
            writer.writerow(item)

if __name__ == "__main__":
    obo_file = 'uberon-basic.obo'  
    main_uberon_with_children, main_uberon_with_mesh_umls = parse_obo_file(obo_file)

    children_fields = ['main_uberon_id', 'children']
    mesh_umls_fields = ['main_uberon_id', 'mesh_ids', 'umls_ids']

    write_to_csv(main_uberon_with_children, 'uberon_main_with_children.csv', children_fields)
    write_to_csv(main_uberon_with_mesh_umls, 'uberon_main_with_mesh_umls.csv', mesh_umls_fields)

    print("CSV files 'uberon_main_with_children.csv' and 'uberon_main_with_mesh_umls.csv' have been created successfully.")
