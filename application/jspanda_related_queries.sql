use jspanda;

select * from jspanda_orders where date between '20200301' and '20200330';

select * from jspanda_orders where `ordered_by` like '%na prodaju%' and is_paid=false;

update jspanda_orders set date='20191118' where date='20191112';

update jspanda_orders set is_na_prodaju = true where `ordered_by` like '%na prodaju%';
update jspanda_orders set is_na_prodaju = false where `ordered_by` not like '%na prodaju%';

update jspanda_orders set is_paid=1 where date="20191101";
delete from jspanda_orders where date='20191108';

# add is_received column
alter table jspanda_orders add column is_received bool after is_paid;
alter table jspanda_orders add column is_na_prodaju bool after extra_notes;

update jspanda_orders set is_received=true;

delete from jspanda_orders where date='20191127';

select * from users;