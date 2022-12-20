select count(*),
	   count(distinct idPlayer),
	   avg(flagSub),
	   sum(flagSub)

from tb_abt_sub