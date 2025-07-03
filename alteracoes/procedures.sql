CREATE OR ALTER PROCEDURE SP_IND_PRODUTOS_EM_PROCESSO
RETURNS (
  OP INTEGER,

  CODPROD INTEGER,
  DESCRICAO Varchar(100),
  ID_PROCESSO INTEGER,
  PROCESSO VARCHAR(60),
  PRODUZIR NUMERIC(15,2),
  PRODUZIDO NUMERIC(15,2),
  QTD_SETOR NUMERIC(15,2),
  DT date,
  PRAZO date,
  status_op VARCHAR(60),
  NOME VARCHAR(60),
  nm INTEGER,
  pd_dt date,
  ESTOQUE VARCHAR(1)
)
AS
DECLARE VARIABLE op_old INTEGER;
DECLARE VARIABLE codprod_old INTEGER;
DECLARE VARIABLE id_processo_old INTEGER;
DECLARE VARIABLE qtd_setor_old NUMERIC(15,2);
DECLARE VARIABLE qtd_produzir_old NUMERIC(15,2);
DECLARE VARIABLE qtd_setor_old_total NUMERIC(15,2);

BEGIN
  op_old = 0;
  codprod_old = 0;
  id_processo_old = 0;
  qtd_setor_old = 0;
  qtd_produzir_old = 0;
  qtd_setor_old_total = 0;

                 FOR SELECT i.op,i.codpro, ic.id as ID1, p.descricao, ic.descricao, SUM(i.qtd),io.dt,cast(io.prazo as date),sp_ind_op_status.status_op,f.nome,pv.nm,pv.dt as pd_dt,ic.estoque
                      FROM ind_op_itens i
                      join pedidovendas pv on pv.nm = i.pedido
                      join funcionarios f on f.codigo = pv.vendedor
                      left join sp_ind_op_status(i.op)  on 1=1
                      join ind_op io on io.id = i.op
                      JOIN prod_processos pp ON pp.codprod = i.codpro
                      join produtos p on p.cod = i.codpro
                      JOIN ind_cadprocessos ic ON ic.id = pp.codprocesso
                      where (sp_ind_op_status.status_op <> 'FINALIZADA')
                      GROUP BY i.op,i.codpro, pp.id, ic.id, ic.descricao, p.descricao,io.prazo,sp_ind_op_status.status_op,f.nome,pv.nm,io.dt,pv.dt,ic.estoque
                      ORDER BY i.op, i.codpro, pp.id

                  INTO
                  :op,
                  :codprod,
                  :id_processo,
                  :descricao,
                  :processo,
                  :produzir,
                  :dt,
                  :prazo,
                  :status_op,
                  :nome,
                  :nm,
                  :pd_dt,
                  :ESTOQUE


   DO
     BEGIN
                     SELECT COALESCE(SUM(ibp.qtd), 0)
                     FROM ind_baixa_processos ibp
                     WHERE
                      ibp.op = :op
                     AND ibp.codprod = :codprod
                     AND ibp.processo = :id_processo
                     AND (ibp.excluido = 'N' OR ibp.excluido IS NULL)
                     INTO :produzido;




    IF (:op <> op_old OR :codprod <> codprod_old) THEN
    BEGIN
      op_old = :op;
      codprod_old = :codprod;
      id_processo_old = :id_processo;
      qtd_setor_old = 0;
      qtd_produzir_old = 0;
      qtd_setor_old_total = 0;
    END

    qtd_setor = :produzir - :produzido - qtd_setor_old_total;





    op_old = :op;
    codprod_old = :codprod;
    id_processo_old = :id_processo;
    qtd_setor_old = qtd_setor;
    qtd_produzir_old = :produzir;
    qtd_setor_old_total = qtd_setor_old_total + qtd_setor_old;

    SUSPEND;
  END
END;


