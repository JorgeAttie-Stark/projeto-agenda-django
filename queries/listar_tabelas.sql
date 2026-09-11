-- Rode com SQLTools: selecione a query e Ctrl/Cmd+E Ctrl/Cmd+E
-- ou clique no ícone de play na query

SELECT name
FROM sqlite_master
WHERE type = 'table'
ORDER BY name;
