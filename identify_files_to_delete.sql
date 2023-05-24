
--run this first, this creates the temp table to hold the IDs which can be used to pull the right files from aws_scrape
create temporary table id_maps(
sample_id varchar(100) not null,
aliquot_id varchar(100) not null,
sequencing_type varchar(100) not null,
tenx_id varchar(100),
kf_biospecimen_id varchar(100))

--dont run these unless needed

--drop table id_maps
--truncate table id_maps
--select * from id_maps


--run this next, this inserts values into the table so they can be used to find the correct files
insert into id_maps(sample_id, aliquot_id, sequencing_type, tenx_id, kf_biospecimen_id)
values
('7316-1464','862550','smartseq','','BS_8HVB4YXV'),
('7316-2069','893189','smartseq','','BS_9R50GXVG'),
('7316-2092','841145','smartseq','','BS_923WT3B1'),
('7316-2100','893182','smartseq','','BS_ZN1ETM5X'),
('7316-2146','841146','smartseq','','BS_DDEGKS2C'),
('7316-2594','841147','smartseq','','BS_ACVGW9P5'),
('7316-2660','479109','smartseq','','BS_KNHJ1P66'),
('7316-2737','893192','smartseq','','BS_0K1VWENJ'),
('7316-2751','893193','smartseq','','BS_M63VFED2'),
('7316-3058','841151','smartseq','','BS_ZH67BMNE'),
('7316-3158','841149','smartseq','','BS_45WGCNDJ'),
('7316-371','862547','smartseq','','BS_R3308SP5'),
('7316-4842','893195','smartseq','','BS_4JCTWGEB'),
('7316-4844','893196','smartseq','','BS_1BDPCTHP'),
('7316-895','901061','smartseq','','BS_YB5N2F8V'),
('7316UP-1962','544767','smartseq','','BS_AZVX4YJX'),
('7316UP-2058','901070','smartseq','','BS_W0SSG6W6'),
('7316UP-2333','900656','smartseq','','BS_21JH0VS8'),
('7316UP-2403','900661','smartseq','','BS_84V1M39F'),
('7316-1464','862551','tenx','HBAD-A-1','BS_4EGMZHXW'),
('7316-2069','893181','tenx','HBAD-B-3','BS_VYFWRABG'),
('7316-2092','841167','tenx','HBAD-B-4','BS_678G3EF3'),
('7316-2146','841168','tenx','HBAD-C-3','BS_QQ8VMMP0'),
('7316-2594','841169','tenx','HBAD-F-2','BS_885NVB2Y'),
('7316-2737','893184','tenx','HBAD-D-1','BS_RGJKRK8S'),
('7316-2751','893185','tenx','HBAD-E4','BS_23MPVS1C'),
('7316-3058','841173','tenx','HBAD-B-1','BS_61XPNTTX'),
('7316-3158','841171','tenx','HBAD-B-2','BS_DMH8A5CB'),
('7316-371','862549','tenx','HBAD-A-4','BS_8PMKPFAJ'),
('7316-4842','893187','tenx','HBAD-C-1','BS_N44BGJ82'),
('7316-4844','893188','tenx','HBAD-C-4','BS_HGP983B9'),
('7316-895','901060','tenx','HBAD-C-2','BS_AJMKVT26'),
('7316UP-2058','901071','tenx','HBAD-A-3',''),
('7316UP-2333','900650','tenx','HBAD-F-1',''),
('7316UP-2403','900655','tenx','HBAD-A-2','')

--pull files from s3 that match on either the sdg_id (for smartseq) or the HBAD ID (for 10x). Only pull from the project-hope directory and ignore md5
with files as (
	select bucket, s3path, file_name, substring(file_name, '7316[A-Z]{0,2}-[0-9]*') as sample_id, 
	translate(substring(file_name, 'HBAD-[A-F]-?[0-9]'), '-','') as tenx_id
from file_metadata.aws_scrape
where bucket='kf-strides-study-us-east-1-prd-sd-bhjxbdqk'
and "key" like 'source/NYGC/project_hope%'
and file_name not like '%md5'),

--modify the tenx id to account for inconsistencies in filenaming
idmaps as(
select sample_id, aliquot_id, sequencing_type, translate(tenx_id, '-','') as tenx_id, kf_biospecimen_id
from id_maps),

--select the final list of files with IDs.  This is where this ends if we just need the original files
final_list as 
(select *
from files
left join idmaps on (files.sample_id=idmaps.sample_id and idmaps.sequencing_type='smartseq') 
	or (files.tenx_id=idmaps.tenx_id and idmaps.sequencing_type='tenx')
where files.sample_id is not null or files.tenx_id is not null)



--add this section to find erroneously registered files
--this takes all the s3 paths from the original files and checks for any cases where there is a file with a GF_ID but there is NO associated sequencing experiment
--this works because the pipeline always errored out before the sequencing experiment info could be included and the associations could be built
--the inverse of this approach (check for files where sequencing experiment DOES exist) results in 12400 which is the correct number of files, confiming this will catch all the "bad" items 


select genomic_file.kf_id, *
from public.genomic_file
inner join final_list on genomic_file.external_id=final_list.s3path
left join public.sequencing_experiment_genomic_file on genomic_file.kf_id=sequencing_experiment_genomic_file.genomic_file_id 
where sequencing_experiment_genomic_file.genomic_file_id  is null
	