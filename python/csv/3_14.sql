# 데이터베이스를 선택
use ubion;

# 데이터베이스에서 emp table의 데이터를 모두 출력
select * from emp;

# emp table에서 SAL 컬럼의 데이터가 1500 이상인 사원의 
# 정보출력
select * 
from emp 
where SAL >= 1500 ;

# emp table에서 job이 manager이고 sal이 1500 이상인
# 사원의 이름을 출력
# 컬럼 조건식(select 뒤): 사원의 이름
# 인덱스 조건식(where): job = 'manager', sal >= 1500 
select `ENAME`
from `emp`
where `job` = 'manager' and `sal` >= 1500;

# emp table에서 sal이 1500이상이고 2500이하인
# 사원의 정보 출력
# case1
select *
from `emp`
where `sal` >= 1500 and `sal` <= 2500;

#case2
select *
from `emp`
where `sal` between 1500 and 2500;

# emp table에서 JOB이 MANAGER이거나 SALESMAN인
# 사원의 정보 출력
# case1 
select *
from `emp`
where `job` = 'MANAGER' or `job` = 'SALESMAN';

# case2
select *
from `emp`
where `job` in ('manager','salesman');

# 사람의 이름이 특정 문자(s) 시작하는 사원의 정보를 출력
select * 
from `emp`
where `ename` like 's%' ;
# 사원의 이름에 특정 문자가 포함되어있는 사원의 정보를 출력
select *
from `emp`
where `ename` like '%a%';
# 사원의 이름이 특정 문자로 끝이 나는 사원이 정보를 출력
select *
from `emp`
where `ename` like '%s';

# 두개의 테이블을 특정 조건에 맞게 열 결합(조인결합)
select *
from `emp` inner join `dept` on `emp`.`deptno` = `dept`.`deptno`
where `loc` = 'chicago';

# 두개의 테이블을 특정 조건에 맞게 열 결합 -> 부서번호가 20인 사원 정보 출력
select *
from `emp` left join  `dept` on `emp`.`deptno`  = `dept`.`deptno` 
where `emp`.`deptno` = 20;

## 부서의 지역이 NEW WORK인 사원의 정보만 출력
# case1
select `empno`, `ename`, `job`
from `emp` A inner join `dept` B 
on A.`deptno` = B.`deptno`
where `loc` = 'new york';
# case2(sub query)
select * 
from `emp`
where `deptno` in (
	select `deptno` 
	from `dept` 
	where `loc` !=  'new york');
    
# 단순한 행 결합 (유니언 결합)
select * 
from `tran_1`
union
select *
from `tran_2`;

# ``를 사용하는 이유
# table의 이름이나 컬럼의 이름에 공백이 존재하는 경우
select *
from `sales records`;

select `item type`, `sales channel` 
from `sales records`;


## 그룹화
## 조건을 처리하고 그룹화 
## 조건 처리 그룹화 조건 처리
## 조건 처리 그룹화 조건 처리 정렬 변경
# sales records에서 대륙별 총이윤의 합계
select `region`, sum(`total profit`) as `Total profit of Region`
from `sales records`
group by `region`
order by `Total profit of Region` desc;

## 국가별(Country)별 총 이윤 (Total Profit)의 합계를 구하고 
## 총 이윤을 기준으로 내림차순 정렬
select `country`, sum(`total profit`) as `tot`
from `sales records`
group by `country`
having `tot` > 28000000
order by `tot` desc
limit 3;

## 아시아의 국가들 중 총 이윤의 합계 높은 5개 국가
select `country` , sum(`total profit`) as `tot`
from `sales records`
where `region` = 'asia'
group by `country`
order by `tot` desc
limit 5;





