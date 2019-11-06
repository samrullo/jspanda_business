use jspanda;
select * from received_money;

select * from jspanda_orders;
delete from jspanda_orders;
show  FULL columns from jspanda_orders;

ALTER TABLE jspanda_orders MODIFY ordered_by VARCHAR(100) CHARACTER SET utf8;
ALTER TABLE jspanda_orders MODIFY extra_notes VARCHAR(400) CHARACTER SET utf8;
ALTER TABLE jspanda_orders MODIFY name VARCHAR(200) CHARACTER SET utf8;

ALTER TABLE jspanda_orders AUTO_INCREMENT = 1;

SELECT character_set_name FROM information_schema.`COLUMNS` 
WHERE table_schema = "jspanda_orders"
  AND table_name = "jspanda_orders"
  AND column_name = "ordered_by";



show columns from family_spending;
select * from users;
ALTER TABLE users
ADD COLUMN login VARCHAR(15) AFTER name;
ALTER TABLE users
ADD COLUMN is_admin bool AFTER last_login;
show columns from shipment_spending;

select * from shipment_weight;
alter table shipment_spending modify `weight` float;
show columns from shipment_weight;
alter table shipment_weight
add column is_paid bool after amount;
alter table shipment_weight modify `weight` float;
alter table shipment_spending modify `date` date;
show columns from visa_spending;
alter table visa_spending modify `date` date;

ALTER DATABASE jspanda CHARACTER SET utf8 COLLATE utf8_general_ci;

SELECT default_character_set_name FROM information_schema.SCHEMATA S WHERE schema_name = "jspanda";

SELECT CCSA.character_set_name FROM information_schema.`TABLES` T,information_schema.`COLLATION_CHARACTER_SET_APPLICABILITY` CCSA WHERE CCSA.collation_name = T.table_collation AND T.table_schema = "jspanda" AND T.table_name = "jspanda_orders";

ALTER TABLE jspanda_orders CONVERT TO CHARACTER SET utf8;
