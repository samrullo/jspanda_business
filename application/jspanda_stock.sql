use jspanda;
show tables;

show table status from jspanda;

select * from family_spending where date='20200201';


update family_spending set date='20200101' where date='20191124';

delete from family_spending where date='20191201' and name="";

select sum(amount) from visa_spending where date='20191130';

show columns from category;
show columns from product;
drop table category;


show columns from stock;


select * from product;
select * from category;
select * from stock;

delete from product;
delete from category;
delete from stock;

alter table category auto_increment=1;
alter table product auto_increment=1;
alter table stock auto_increment=1;

ALTER TABLE product CONVERT TO CHARACTER SET utf8;
ALTER TABLE product MODIFY `name` VARCHAR(500) CHARACTER SET utf8;

SELECT CCSA.character_set_name FROM information_schema.`TABLES` T,information_schema.`COLLATION_CHARACTER_SET_APPLICABILITY` CCSA 
WHERE CCSA.collation_name = T.table_collation 
AND T.table_schema = "jspanda" 
AND T.table_name = "product";

# view column character set
SELECT character_set_name FROM information_schema.`COLUMNS` 
WHERE table_schema = "schema"
  AND table_name = "category"
  AND column_name = "name";



drop table product_category;
drop table product;
drop table category;