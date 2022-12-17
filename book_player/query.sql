
/* 
VERIFICAR O PRIMEIRO E ULTIMO DIA DE REGISTRO DOS JOGADORES
-------------------------------------------
 SELECT MIN(dtCreatedAt),
        MAX(dtCreatedAt)

FROM tb_lobby_stats_player

*/


/*
QUERY PARA CHAMAR OS PLAYERS DE APENAS 30 DIAS,
PERIODO ALINHADO PARA ANALISE, POIS SÓ TEMOS 6
MESES DE DADOS
---------------------------------------------

SELECT date(dtCreatedAt),
    COUNT(*)

FROM tb_lobby_stats_player

WHERE dtCreatedAt < '{date}'
AND dtCreatedAt > DATE ('{date}', '-30 DAY')

GROUP BY DATE(dtCreatedAt)
ORDER BY date(dtCreatedAt)
*/

/*
****************************************
CHAMAR TODOS AS FEATURES DA TABELA LOBBY STATS
NO PERIODO DE -30 DIAS A CONTAR DO DIA 01-02-22
----------------------------------------------
SELECT * FROM tb_lobby_stats_player

WHERE dtCreatedAt < '{date}'
AND dtCreatedAt > DATE('{date}', '-30 DAY')
*/

/*ESTATÍSTICA_01 - QUANT DE PARTIDAS POR ID DE
JOGADOR - USANDO A FUNÇÃO 'DISTINCT' QUE
SERVE PARA ELIMINAR OS DUPLICADOS SOMANDO SEUS VALORES */


WITH tb_lobby as(

    --VIEW COM OS FILTROS DE DATA

    SELECT * 
    FROM tb_lobby_stats_player
    WHERE dtCreatedAt < '{date}'
    AND dtCreatedAt > DATE('{date}', '-30 DAY')
),


 --TABELA COM TODAS AS ESTATISTICAS
tb_stats as(


    SELECT idPlayer,
        COUNT(DISTINCT idLobbyGame) AS qtPartidas,
                /* CRIAMOS UMA VARIAVEL PARA SABER SE COMPLETOU A PARTIDA(ACIMA DE 16 ROUNDS*/
        COUNT(DISTINCT CASE WHEN qtRoundsPlayed < 16 THEN idLobbyGame END) AS qtPartidasMenos16,
        COUNT(DISTINCT DATE(dtCreatedAt)) AS qtDias,
        min(julianday('{date}')- julianday(dtCreatedAt)) as qtDiasUltimaLobby,
        1.0 * COUNT(DISTINCT idLobbyGame) / COUNT(DISTINCT DATE(dtCreatedAt)) AS mediaPartidasDia,
        /*VAMOS CRIAR A MEDIA DAS FEATURES - USAMOS A FUNÇÃO 'AVG' - TECNICA DE MANIPULAR VARIAS
        VARIAVEIS COM SHIFT+ALT+I E UPPCASE*/
        avg(qtKill) as avgQtKill,
        avg(qtAssist) as avgQtAssist,
        avg(qtDeath) as avgQtDeath,
        avg(1.0*(qtKill+qtAssist)/qtDeath) as avgKDA,--MEDIA ENTRE ELIMINAÇÕES+ASSIT / MORTE DO PLAYER
        1.0*sum(qtKill+qtAssist)/sum(qtDeath) as KDAgeral,--SUMA DAS MEDIAS ENTRE ELIMINAÇÕES+ASSIT / MORTE DO PLAYER
        avg(1.0*(qtKill+qtAssist)/qtRoundsPlayed) as avgKARound,--MEDIA ENTRE ELIMINAÇÕES+ASSIT / ROUNDS DO PLAYER
        1.0*sum(qtKill+qtAssist)/sum(qtRoundsPlayed) as KARoundGeral,--SUMA DAS MEDIAS ENTRE ELIMINAÇÕES+ASSIT / ROUNDS DO PLAYER
        avg(qtHs) as avgQtHs, --Hs são mortes por tiro na cabeça
        avg(1.0* qtHs/qtKill) as avgHsRate, --MEDIA DE MORTES COM TIRO NA CABEÇA
        1.0*sum(qtHs)/sum(qtKill) as txHsGeral, -- SOMA DE MORTES PELA SOMA DE TIRO NA CABEÇA
        avg(qtBombeDefuse) as avgQtBombeDefuse,
        avg(qtBombePlant) as avgQtBombePlant,
        avg(qtTk) as avgQtTk,
        avg(qtTkAssist) as avgQtTkAssist,
        avg(qt1Kill) as avgQt1Kill,
        avg(qt2Kill) as avgQt2Kill,
        avg(qt3Kill) as avgQt3Kill,
        avg(qt4Kill) as avgQt4Kill,
        avg(qt5Kill) as avgQt5Kill,
        avg(qtPlusKill) as avgQtPlusKill,
        avg(qtFirstKill) as avgQtFirstKill,
        avg(vlDamage) as avgVlDamage,--QUANT DE DANO FOI GERADO NO ADVERSARIO
        avg(1.0* vlDamage/qtRoundsPlayed) as avgDamageRound,--QUANT DE DANO POR ROUND
        1.0*sum(vlDamage)/sum(qtRoundsPlayed) as DamageRoundGeral, --A MEDIA DA SOMA DE DANOS PELA SOMA DE ROUNDS
        avg(qtHits) as avgQtHits,
        avg(qtShots) as avgQtShots,
        avg(qtLastAlive) as avgQtLastAlive,
        avg(qtClutchWon) as avgQtClutchWon,
        avg(qtRoundsPlayed) as avgQtRoundsPlayed,
        avg(vlLevel) as avgVlLevel,
        avg(qtSurvived) as avgQtSurvived,
        avg(qtTrade) as avgQtTrade,
        avg(qtFlashAssist) as avgQtFlashAssist,
        avg(qtHitHeadshot) as avgQtHitHeadshot,
        avg(qtHitChest) as avgQtHitChest,
        avg(qtHitStomach) as avgQtHitStomach,
        avg(qtHitLeftAtm) as avgQtHitLeftAtm,
        avg(qtHitRightArm) as avgQtHitRightArm,
        avg(qtHitLeftLeg) as avgQtHitLeftLeg,
        avg(qtHitRightLeg) as avgQtHitRightLeg,
        avg(flWinner) as avgFlWinner,

        /*CRIAMOS VARIAVEIS PARA CADA MAPA UTILIZADO PELOS PLAYERS POIS 
        DEPENDENDO DO MAPA JOGADO SABEREMOS SE ESTA TREINANDO OU JOGANDO 
        VALENDO*/

        /* CRIAMOS VARIAVEIS PARA QUANT DE VITORIAS POR MAPA */
        
        count(distinct case when descMapName = "de_mirage" then idLobbyGame end) as qtMiragePartidas,
        count(distinct case when descMapName = "de_mirage" and flWinner = 1 then idLobbyGame end) as qtMirageVitorias,
        count(distinct case when descMapName = "de_nuke" then idLobbyGame end) as qtNukePartidas,
        count(distinct case when descMapName = "de_nuke" and flWinner = 1 then idLobbyGame end) as qtNukeVitorias,
        count(distinct case when descMapName = "de_inferno" then idLobbyGame end) as qtInfernoPartidas,
        count(distinct case when descMapName = "de_inferno" and flWinner = 1 then idLobbyGame end) as qtInfernoVitorias,
        count(distinct case when descMapName = "de_vertigo" then idLobbyGame end) as qtVertigoPartidas,
        count(distinct case when descMapName = "de_vertigo" and flWinner = 1 then idLobbyGame end) as qtVertigoVitorias,
        count(distinct case when descMapName = "de_ancient" then idLobbyGame end) as qtAncientPartidas,
        count(distinct case when descMapName = "de_ancient" and flWinner = 1 then idLobbyGame end) as qtAncientVitorias,
        count(distinct case when descMapName = "de_dust2" then idLobbyGame end) as qtDust2Partidas,
        count(distinct case when descMapName = "de_dust2" and flWinner = 1 then idLobbyGame end) as qtDust2Vitorias,
        count(distinct case when descMapName = "de_train" then idLobbyGame end) as qtTrainPartidas,
        count(distinct case when descMapName = "de_train" and flWinner = 1 then idLobbyGame end) as qtTrainVitorias,
        count(distinct case when descMapName = "de_overpass" then idLobbyGame end) as qtOverpassPartidas,
        count(distinct case when descMapName = "de_overpass" and flWinner = 1 then idLobbyGame end) as qtOverpassVitorias

    
    

    FROM tb_lobby


    GROUP BY idPlayer
),

tb_lvl_atual as (
    --ENCONTRAR O ULTIMO LEVEL(NIVEL) DO PLAYER
    SELECT idPlayer,
        vlLevel
    --SUBQUERY
    FROM(
        SELECT 
            idLobbyGame,
            idPlayer,
            vlLevel,
            dtCreatedAt,
            row_number() over (PARTITION BY idPlayer ORDER BY dtCreatedAt desc)as rn

        FROM tb_lobby
    )

    WHERE rn = 1
),

tb_book_lobby as(
    --UNIR AS DUAS VIEWS
    select t1.*,
        t2.vlLevel as vlLevelAtual
    from tb_stats as t1

    left join tb_lvl_atual as t2
    on t1.idPlayer = t2.idPlayer

),
-- Tabela para analisar quais Players possuiam medalhas e se estavam ativas
-- dentro do periodo
tb_medals as (

    select *
    from tb_players_medalha as t1 --selecionar todos os campos da tabela e dar o alias de t1

    left join tb_medalha as t2 -- definir a tabela tb_medalha com t2 e unir a t1,
    on t1.idMedal = t2.idMedal-- usando o campo idMedal como chave principal pois possue nas duas tabelas

    where dtCreatedAt < dtExpiration -- onde data da experição seja menos que a data da criação
    and dtCreatedAt < '{date}' -- e a data da seja o dia do periodo que estamos analisando
    and coalesce(dtRemove, dtExpiration) > date('{date}', '-30 day') -- usando o coalesce caso o valor da linha
    --no campo dtRemove seja null preencher com a data da ultima expiração

),
-- TABELA PARA ANALISAR AS MEDALHAS DOS PLAYERS
tb_book_medal as(

select idPlayer,
       count(distinct idMedal) as qtMedalhaDist, --contar a quantidade de medalhas por player e criar distinção
            -- criar campo quantidade de medalhas adquiridas com data da criação denro do periodo 
       count(distinct case when dtCreatedAt > date('{date}', '-30 day') then id end) as qtMedalhaAdquiridas,
            --criar variavel quant medalhas premium(caso o valor do campo for 'Medalha Premium' substitua
            --por 1 caso não substitua por 0)
       sum( case when descMedal = 'Membro Premium' then 1 else 0 end) as qtPremium,
            --criar variavel quant medalhas premium(caso o valor do campo for 'Medalha Plus' substitua
            --por 1 caso não substitua por 0)
       sum( case when descMedal = 'Membro Plus' then 1 else 0 end) as qtPlus,
            --criar variavel assinatura ativa onde caso a variavel desMedal em 'Membro Premium','Membro Plus'
         -- for maior ou igual a data {date} se for substitua por 1 senão substitua por 0
       max( case when descMedal in ('Membro Premium','Membro Plus')
                      and coalesce(dtRemove, dtExpiration)>= '{date}'
                      then 1 else 0 end) as AssinaturaAtiva

from tb_medals

group by idPlayer


)

insert into tb_book_player

select '{date}' as dtRef,
       t1.*,
       coalesce(t2.qtMedalhaDist,0) as qtMedalhaDist,
       coalesce(t2.qtMedalhaAdquiridas,0) as qtMedalhaAdquiridas,
       coalesce(t2.qtPremium,0) as qtPremium,
       coalesce(t2.qtPlus,0) as qtPlus,
       coalesce(t2.AssinaturaAtiva,0) as AssinaturaAtiva,

       t3.flFacebook,
       t3.flTwitter,
       t3.flTwitch,
       t3.descCountry,
       t3.dtBirth,
       ((JulianDay('{date}')) - JulianDay(t3.dtBirth))/365.25 as vlIdade,
       (JulianDay('{date}')) - JulianDay(t3.dtRegistration)as vlDiasCadastro


from tb_book_lobby as t1

left join tb_book_medal as t2
on t1.idPlayer = t2.idPlayer

left join tb_players as t3
on t1.idPlayer = t3.idplayer;