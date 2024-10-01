SELECT
	nick_name as '参与人员昵称',
	phone as '参与人员手机号',
	has_official_accounts as '是否关注微信号',
	last_login_date as '最后登录时间'
FROM
	`wanxinxinli_cloud_prod`.`talktime_common_client_user` 
WHERE
	`ad_type` = '182' 
	OR `user_json` LIKE '%%182%%'
ORDER BY
	`ad_type` DESC