def build_graph(files):
    nodes = {}
    edges = []
    def add_node(node_id, label, group):
        nodes[node_id] = {"id": node_id, "label": label, "group": group}

    for f in files[:80]:
        file_id = "file:" + f.path
        add_node(file_id, f.path, "file")
        for name, finding in f.findings.items():
            entity_id = "entity:" + name
            add_node(entity_id, name, "entity")
            edges.append({"from": file_id, "to": entity_id, "label": str(finding.count)})
            for sample in finding.samples[:2]:
                sample_id = f"sample:{name}:{sample}"
                add_node(sample_id, sample, "sample")
                edges.append({"from": entity_id, "to": sample_id, "label": "sample"})
    return {"nodes": list(nodes.values()), "edges": edges[:300]}
