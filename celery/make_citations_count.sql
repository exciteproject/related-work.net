select meta_id_source, count(meta_id_target) as citations from matches group by meta_id_source;