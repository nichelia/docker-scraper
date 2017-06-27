#!/usr/bin/python
import sys, os
sys.path.append( os.getcwd() )


import unittest
import time
from nhsbot.spiders.nhs_uk import NHSChoices
from responses import fake_response_from_file

class NHSChoicesSpiderTest(unittest.TestCase):

    def setUp(self):
        self.spider = NHSChoices()

    def _test_extracted_item(self, item_content, expected_length, attributes):
        count = len(item_content)

        for item in item_content:
            self.assertIsNotNone(item_content[item])
        
        self.assertItemsEqual(item_content, attributes)
        self.assertEqual(count, expected_length)


    def _test_extracted_item_content(self, item_content, valid_content):
        for item in item_content:
            if isinstance(item_content[item], dict):
                for content in item_content[item]:
                    self.assertEqual(item_content[item][content], valid_content[item][content])
            else:
                self.assertEqual(item_content[item], valid_content[item])


    def test_valid_parse(self):
        expected_length = 8
        attributes = ['source', 'crawled_epoch_date', 'id', 'url', 'title', 'meta', 'content', 'last_reviewed_epoch_date']
        valid_content = {
                         'source': 'nhsuk-spider',
                         'crawled_epoch_date': int(time.time()),
                         'id': 'http://www.example.com',
                         'url': 'http://www.example.com',
                         'title': u'Abdominal aortic aneurysm\xa0',
                         'meta': { 
                                  'DC.rights': 'http://www.nhs.uk/termsandconditions/Pages/TermsConditions.aspx',
                                  'DCSext.RealUrl': '/conditions/repairofabdominalaneurysm/Pages/Introduction.aspx',
                                  'DC.coverage': 'England',
                                  'keywords': "National Health Service (NHS),Abdominal aortic aneurysm,aneurysm,rupture,screening",
                                  "DC.title": "Abdominal aortic aneurysm - NHS Choices",
                                  "DC.language": "eng",
                                  "WT.ti": "Abdominal aortic aneurysm - NHS Choices",
                                  "WT.cg_n": "Treatments and Conditions",
                                  "DC.creator": "NHS Choices",
                                  "WT.sv": "CH-P-WEB02",
                                  "WT.cg_s": "Abdominal aortic aneurysm",
                                  'description': u'An abdominal aortic aneurysm (AAA) is a swelling (aneurysm) of the aorta \u2013 the main blood vessel that leads away from the heart, down through the abdomen to the rest of the body. ',
                                  "DC.identifier": "http://www.nhs.uk",
                                  "eGMS.accessibility": "Double-A",
                                  "DCSext.Server": "CH-P-WEB02",
                                  "DCSext.BM_Section2": "Abdominal aortic aneurysm",
                                  "DCSext.BM_Section3": "Repair Of Abdominal Aortic Aneurysm",
                                  "DCSext.BM_Section1": "Treatments and Conditions",
                                  "DC.subject": "National Health Service (NHS),Abdominal aortic aneurysm,aneurysm,rupture,screening",
                                  'DC.format': u'text/html',
                                  'DC.publisher': u'Department of Health',
                                  'DC.Subject': u'ID707 ID864 ID1933',
                                  'DC.description': u'An abdominal aortic aneurysm (AAA) is a swelling (aneurysm) of the aorta \u2013 the main blood vessel that leads away from the heart, down through the abdomen to the rest of the body. '
                                 },
                         'content': u'Introduction\xa0 An abdominal aortic aneurysm (AAA) is a swelling (aneurysm) of the aorta\xa0 \u2013\xa0 the main blood vessel that\xa0leads away\xa0from the heart, down through the abdomen to the rest of the body. The abdominal aorta is the largest blood vessel in the body and is usually around 2cm wide\xa0 \u2013\xa0 roughly the width of a garden hose. However, it can swell to over 5.5cm\xa0 \u2013\xa0 what doctors class as a large AAA. Large aneurysms are rare, but can be very serious. If a large aneurysm bursts, it causes huge internal bleeding and is usually fatal. The bulging occurs when the wall of the aorta weakens. Although what causes this weakness is unclear, smoking and high blood pressure are thought to increase the risk of an aneurysm.  AAAs are most common in men aged over 65. A rupture accounts for more than 1 in 50 of all deaths in this group and a total of 6,000 deaths in England and Wales each year.  This is why all men are invited for a\xa0 screening test  when they turn 65. The test involves a simple  ultrasound scan , which takes around 10-15 minutes. Symptoms of an AAA In most cases, an AAA causes no noticeable symptoms. However, if it becomes large, some people may develop a pain or a pulsating feeling in their\xa0abdomen (tummy)\xa0or persistent back pain. An AAA doesn\u2019t usually pose a serious threat to health, but there\u2019s a risk that a larger aneurysm could burst (rupture).  A ruptured aneurysm can cause massive internal bleeding, which is usually fatal. Around 8 out of 10 people with a rupture either die before they reach hospital or don\u2019t survive surgery. The most common symptom of a ruptured aortic aneurysm is sudden and severe pain in the abdomen.  If you suspect that you or someone else has had a ruptured aneurysm, call 999 immediately and ask for an ambulance. Read more about the  symptoms of an AAA . Causes of an AAA It\'s not known exactly what causes the aortic wall to weaken, although increasing age and being male are known to be the biggest risk factors. There are other risk factors you can do something about, including smoking and having high blood pressure and cholesterol level. Having a family history of aortic aneurysms also means that you have an increased risk of developing one yourself. Read more about the  causes of an AAA . Diagnosing an AAA Because AAAs usually cause no symptoms, they tend to be diagnosed either as a result of screening or during a routine examination\xa0 \u2013\xa0 for example, if a GP notices a pulsating sensation in your abdomen. The screening test is an\xa0 ultrasound scan ,\xa0which allows the size of your abdominal aorta to be measured on a monitor. This is also how an aneurysm will be diagnosed if your doctor suspects you have one. Read more about  diagnosing an AAA . Treating an AAA If a large AAA is detected before it ruptures, most people will be advised to have treatment, to prevent\xa0it rupturing.  This is usually done with surgery to replace the weakened section of the blood vessel with a piece of synthetic tubing.  If surgery is not advisable \u2013 or if you decide not to have it \u2013 there are a number of non-surgical treatments that can reduce the risk of an aneurysm rupturing.  They include medications to lower\xa0 your cholesterol  and  blood pressure , and  quitting smoking .  You will also have the size of your aneurysm checked regularly with ultrasound scanning. Read more about  treating AAAs . Prevention The best way to prevent getting an aneurysm\xa0 \u2013 \xa0or reduce the risk of an aneurysm growing bigger and possibly rupturing\xa0 \u2013 \xa0is to avoid anything that could damage your blood vessels, such as: \n     smoking  \n     eating a high-fat diet  \n     not exercising regularly  \n     being overweight or obese  \n Read more about  preventing aneurysms . Screening Men who are 65 and over are offered a screening test to check if they have an AAA.  All men in England are invited for screening in the year they turn 65.  Men who are over 65 and have not previously been screened can request a screening test by contacting their\xa0 local AAA screening service  directly.  Women and men under 65 are not invited for screening.  However, if you feel you have an increased risk of having an AAA, talk to your GP who can still refer you for a scan. Read more about  screening for an AAA . \n\n     \n\n       \n               What is an aneurysm? \n An aneurysm is a bulge in a blood vessel caused by a weakness in the blood vessel wall. \n As blood passes through the weakened blood vessel, the blood pressure causes it to bulge outwards. \n Exactly what causes the blood vessel wall to weaken is unclear, though hardening of the arteries, smoking and high blood pressure are thought to increase the risk of an aneurysm. \n Aneurysms can occur anywhere in the body, but the two most common places for them to form are in the abdominal aorta and the brain. \n A burst abdominal aortic aneurysm is also a medical emergency and is usually fatal. \n\n            ',
                         'last_reviewed_epoch_date': 1409356800
                        }

        parsed_condition_page = self.spider.parse_condition(fake_response_from_file('templates/abdominal_aortic_aneurysm.html'))

        self._test_extracted_item(parsed_condition_page, expected_length, attributes)
        self._test_extracted_item_content(parsed_condition_page, valid_content)


    def test_missing_title_parse(self):
        """
            Parsed page should not have a title value.
        """
        expected_length = 7
        attributes = ['source', 'crawled_epoch_date', 'id', 'url', 'meta', 'content', 'last_reviewed_epoch_date']
        valid_content = {
                         'source': 'nhsuk-spider',
                         'crawled_epoch_date': int(time.time()),
                         'id': 'http://www.example.com',
                         'url': 'http://www.example.com',
                         'meta': { 
                                  'DC.rights': 'http://www.nhs.uk/termsandconditions/Pages/TermsConditions.aspx',
                                  'DCSext.RealUrl': '/conditions/repairofabdominalaneurysm/Pages/Introduction.aspx',
                                  'DC.coverage': 'England',
                                  'keywords': "National Health Service (NHS),Abdominal aortic aneurysm,aneurysm,rupture,screening",
                                  "DC.title": "Abdominal aortic aneurysm - NHS Choices",
                                  "DC.language": "eng",
                                  "WT.ti": "Abdominal aortic aneurysm - NHS Choices",
                                  "WT.cg_n": "Treatments and Conditions",
                                  "DC.creator": "NHS Choices",
                                  "WT.sv": "CH-P-WEB02",
                                  "WT.cg_s": "Abdominal aortic aneurysm",
                                  'description': u'An abdominal aortic aneurysm (AAA) is a swelling (aneurysm) of the aorta \u2013 the main blood vessel that leads away from the heart, down through the abdomen to the rest of the body. ',
                                  "DC.identifier": "http://www.nhs.uk",
                                  "eGMS.accessibility": "Double-A",
                                  "DCSext.Server": "CH-P-WEB02",
                                  "DCSext.BM_Section2": "Abdominal aortic aneurysm",
                                  "DCSext.BM_Section3": "Repair Of Abdominal Aortic Aneurysm",
                                  "DCSext.BM_Section1": "Treatments and Conditions",
                                  "DC.subject": "National Health Service (NHS),Abdominal aortic aneurysm,aneurysm,rupture,screening",
                                  'DC.format': u'text/html',
                                  'DC.publisher': u'Department of Health',
                                  'DC.Subject': u'ID707 ID864 ID1933',
                                  'DC.description': u'An abdominal aortic aneurysm (AAA) is a swelling (aneurysm) of the aorta \u2013 the main blood vessel that leads away from the heart, down through the abdomen to the rest of the body. '
                                 },
                         'content': u'Introduction\xa0 An abdominal aortic aneurysm (AAA) is a swelling (aneurysm) of the aorta\xa0 \u2013\xa0 the main blood vessel that\xa0leads away\xa0from the heart, down through the abdomen to the rest of the body. The abdominal aorta is the largest blood vessel in the body and is usually around 2cm wide\xa0 \u2013\xa0 roughly the width of a garden hose. However, it can swell to over 5.5cm\xa0 \u2013\xa0 what doctors class as a large AAA. Large aneurysms are rare, but can be very serious. If a large aneurysm bursts, it causes huge internal bleeding and is usually fatal. The bulging occurs when the wall of the aorta weakens. Although what causes this weakness is unclear, smoking and high blood pressure are thought to increase the risk of an aneurysm.  AAAs are most common in men aged over 65. A rupture accounts for more than 1 in 50 of all deaths in this group and a total of 6,000 deaths in England and Wales each year.  This is why all men are invited for a\xa0 screening test  when they turn 65. The test involves a simple  ultrasound scan , which takes around 10-15 minutes. Symptoms of an AAA In most cases, an AAA causes no noticeable symptoms. However, if it becomes large, some people may develop a pain or a pulsating feeling in their\xa0abdomen (tummy)\xa0or persistent back pain. An AAA doesn\u2019t usually pose a serious threat to health, but there\u2019s a risk that a larger aneurysm could burst (rupture).  A ruptured aneurysm can cause massive internal bleeding, which is usually fatal. Around 8 out of 10 people with a rupture either die before they reach hospital or don\u2019t survive surgery. The most common symptom of a ruptured aortic aneurysm is sudden and severe pain in the abdomen.  If you suspect that you or someone else has had a ruptured aneurysm, call 999 immediately and ask for an ambulance. Read more about the  symptoms of an AAA . Causes of an AAA It\'s not known exactly what causes the aortic wall to weaken, although increasing age and being male are known to be the biggest risk factors. There are other risk factors you can do something about, including smoking and having high blood pressure and cholesterol level. Having a family history of aortic aneurysms also means that you have an increased risk of developing one yourself. Read more about the  causes of an AAA . Diagnosing an AAA Because AAAs usually cause no symptoms, they tend to be diagnosed either as a result of screening or during a routine examination\xa0 \u2013\xa0 for example, if a GP notices a pulsating sensation in your abdomen. The screening test is an\xa0 ultrasound scan ,\xa0which allows the size of your abdominal aorta to be measured on a monitor. This is also how an aneurysm will be diagnosed if your doctor suspects you have one. Read more about  diagnosing an AAA . Treating an AAA If a large AAA is detected before it ruptures, most people will be advised to have treatment, to prevent\xa0it rupturing.  This is usually done with surgery to replace the weakened section of the blood vessel with a piece of synthetic tubing.  If surgery is not advisable \u2013 or if you decide not to have it \u2013 there are a number of non-surgical treatments that can reduce the risk of an aneurysm rupturing.  They include medications to lower\xa0 your cholesterol  and  blood pressure , and  quitting smoking .  You will also have the size of your aneurysm checked regularly with ultrasound scanning. Read more about  treating AAAs . Prevention The best way to prevent getting an aneurysm\xa0 \u2013 \xa0or reduce the risk of an aneurysm growing bigger and possibly rupturing\xa0 \u2013 \xa0is to avoid anything that could damage your blood vessels, such as: \n     smoking  \n     eating a high-fat diet  \n     not exercising regularly  \n     being overweight or obese  \n Read more about  preventing aneurysms . Screening Men who are 65 and over are offered a screening test to check if they have an AAA.  All men in England are invited for screening in the year they turn 65.  Men who are over 65 and have not previously been screened can request a screening test by contacting their\xa0 local AAA screening service  directly.  Women and men under 65 are not invited for screening.  However, if you feel you have an increased risk of having an AAA, talk to your GP who can still refer you for a scan. Read more about  screening for an AAA . \n\n     \n\n       \n               What is an aneurysm? \n An aneurysm is a bulge in a blood vessel caused by a weakness in the blood vessel wall. \n As blood passes through the weakened blood vessel, the blood pressure causes it to bulge outwards. \n Exactly what causes the blood vessel wall to weaken is unclear, though hardening of the arteries, smoking and high blood pressure are thought to increase the risk of an aneurysm. \n Aneurysms can occur anywhere in the body, but the two most common places for them to form are in the abdominal aorta and the brain. \n A burst abdominal aortic aneurysm is also a medical emergency and is usually fatal. \n\n            ',
                         'last_reviewed_epoch_date': 1409356800
                        }

        parsed_condition_page = self.spider.parse_condition(fake_response_from_file('templates/missing_title_abdominal_aortic_aneurysm.html'))

        self._test_extracted_item(parsed_condition_page, expected_length, attributes)
        self._test_extracted_item_content(parsed_condition_page, valid_content)


    def test_multiple_titles_parse(self):
        """
            Parsed page should only have the first found title as a value.
        """
        expected_length = 8
        attributes = ['source', 'crawled_epoch_date', 'id', 'url', 'title', 'meta', 'content', 'last_reviewed_epoch_date']
        valid_content = {
                         'source': 'nhsuk-spider',
                         'crawled_epoch_date': int(time.time()),
                         'id': 'http://www.example.com',
                         'url': 'http://www.example.com',
                         'title': u'Abdominal aortic aneurysm\xa0',
                         'meta': { 
                                  'DC.rights': 'http://www.nhs.uk/termsandconditions/Pages/TermsConditions.aspx',
                                  'DCSext.RealUrl': '/conditions/repairofabdominalaneurysm/Pages/Introduction.aspx',
                                  'DC.coverage': 'England',
                                  'keywords': "National Health Service (NHS),Abdominal aortic aneurysm,aneurysm,rupture,screening",
                                  "DC.title": "Abdominal aortic aneurysm - NHS Choices",
                                  "DC.language": "eng",
                                  "WT.ti": "Abdominal aortic aneurysm - NHS Choices",
                                  "WT.cg_n": "Treatments and Conditions",
                                  "DC.creator": "NHS Choices",
                                  "WT.sv": "CH-P-WEB02",
                                  "WT.cg_s": "Abdominal aortic aneurysm",
                                  'description': u'An abdominal aortic aneurysm (AAA) is a swelling (aneurysm) of the aorta \u2013 the main blood vessel that leads away from the heart, down through the abdomen to the rest of the body. ',
                                  "DC.identifier": "http://www.nhs.uk",
                                  "eGMS.accessibility": "Double-A",
                                  "DCSext.Server": "CH-P-WEB02",
                                  "DCSext.BM_Section2": "Abdominal aortic aneurysm",
                                  "DCSext.BM_Section3": "Repair Of Abdominal Aortic Aneurysm",
                                  "DCSext.BM_Section1": "Treatments and Conditions",
                                  "DC.subject": "National Health Service (NHS),Abdominal aortic aneurysm,aneurysm,rupture,screening",
                                  'DC.format': u'text/html',
                                  'DC.publisher': u'Department of Health',
                                  'DC.Subject': u'ID707 ID864 ID1933',
                                  'DC.description': u'An abdominal aortic aneurysm (AAA) is a swelling (aneurysm) of the aorta \u2013 the main blood vessel that leads away from the heart, down through the abdomen to the rest of the body. '
                                 },
                         'content': u'Introduction\xa0 An abdominal aortic aneurysm (AAA) is a swelling (aneurysm) of the aorta\xa0 \u2013\xa0 the main blood vessel that\xa0leads away\xa0from the heart, down through the abdomen to the rest of the body. The abdominal aorta is the largest blood vessel in the body and is usually around 2cm wide\xa0 \u2013\xa0 roughly the width of a garden hose. However, it can swell to over 5.5cm\xa0 \u2013\xa0 what doctors class as a large AAA. Large aneurysms are rare, but can be very serious. If a large aneurysm bursts, it causes huge internal bleeding and is usually fatal. The bulging occurs when the wall of the aorta weakens. Although what causes this weakness is unclear, smoking and high blood pressure are thought to increase the risk of an aneurysm.  AAAs are most common in men aged over 65. A rupture accounts for more than 1 in 50 of all deaths in this group and a total of 6,000 deaths in England and Wales each year.  This is why all men are invited for a\xa0 screening test  when they turn 65. The test involves a simple  ultrasound scan , which takes around 10-15 minutes. Symptoms of an AAA In most cases, an AAA causes no noticeable symptoms. However, if it becomes large, some people may develop a pain or a pulsating feeling in their\xa0abdomen (tummy)\xa0or persistent back pain. An AAA doesn\u2019t usually pose a serious threat to health, but there\u2019s a risk that a larger aneurysm could burst (rupture).  A ruptured aneurysm can cause massive internal bleeding, which is usually fatal. Around 8 out of 10 people with a rupture either die before they reach hospital or don\u2019t survive surgery. The most common symptom of a ruptured aortic aneurysm is sudden and severe pain in the abdomen.  If you suspect that you or someone else has had a ruptured aneurysm, call 999 immediately and ask for an ambulance. Read more about the  symptoms of an AAA . Causes of an AAA It\'s not known exactly what causes the aortic wall to weaken, although increasing age and being male are known to be the biggest risk factors. There are other risk factors you can do something about, including smoking and having high blood pressure and cholesterol level. Having a family history of aortic aneurysms also means that you have an increased risk of developing one yourself. Read more about the  causes of an AAA . Diagnosing an AAA Because AAAs usually cause no symptoms, they tend to be diagnosed either as a result of screening or during a routine examination\xa0 \u2013\xa0 for example, if a GP notices a pulsating sensation in your abdomen. The screening test is an\xa0 ultrasound scan ,\xa0which allows the size of your abdominal aorta to be measured on a monitor. This is also how an aneurysm will be diagnosed if your doctor suspects you have one. Read more about  diagnosing an AAA . Treating an AAA If a large AAA is detected before it ruptures, most people will be advised to have treatment, to prevent\xa0it rupturing.  This is usually done with surgery to replace the weakened section of the blood vessel with a piece of synthetic tubing.  If surgery is not advisable \u2013 or if you decide not to have it \u2013 there are a number of non-surgical treatments that can reduce the risk of an aneurysm rupturing.  They include medications to lower\xa0 your cholesterol  and  blood pressure , and  quitting smoking .  You will also have the size of your aneurysm checked regularly with ultrasound scanning. Read more about  treating AAAs . Prevention The best way to prevent getting an aneurysm\xa0 \u2013 \xa0or reduce the risk of an aneurysm growing bigger and possibly rupturing\xa0 \u2013 \xa0is to avoid anything that could damage your blood vessels, such as: \n     smoking  \n     eating a high-fat diet  \n     not exercising regularly  \n     being overweight or obese  \n Read more about  preventing aneurysms . Screening Men who are 65 and over are offered a screening test to check if they have an AAA.  All men in England are invited for screening in the year they turn 65.  Men who are over 65 and have not previously been screened can request a screening test by contacting their\xa0 local AAA screening service  directly.  Women and men under 65 are not invited for screening.  However, if you feel you have an increased risk of having an AAA, talk to your GP who can still refer you for a scan. Read more about  screening for an AAA . \n\n     \n\n       \n               What is an aneurysm? \n An aneurysm is a bulge in a blood vessel caused by a weakness in the blood vessel wall. \n As blood passes through the weakened blood vessel, the blood pressure causes it to bulge outwards. \n Exactly what causes the blood vessel wall to weaken is unclear, though hardening of the arteries, smoking and high blood pressure are thought to increase the risk of an aneurysm. \n Aneurysms can occur anywhere in the body, but the two most common places for them to form are in the abdominal aorta and the brain. \n A burst abdominal aortic aneurysm is also a medical emergency and is usually fatal. \n\n            ',
                         'last_reviewed_epoch_date': 1409356800
                        }

        parsed_condition_page = self.spider.parse_condition(fake_response_from_file('templates/multiple_titles_abdominal_aortic_aneurysm.html'))

        self._test_extracted_item(parsed_condition_page, expected_length, attributes)
        self._test_extracted_item_content(parsed_condition_page, valid_content)


    def test_empty_parse(self):
        """
            Parsed page should only have the four standard attributes we set from the spider.
        """
        expected_length = 4
        attributes = ['source', 'crawled_epoch_date', 'id', 'url']
        valid_content = {
                         'source': 'nhsuk-spider',
                         'crawled_epoch_date': int(time.time()),
                         'id': 'http://www.example.com',
                         'url': 'http://www.example.com',
                        }

        parsed_condition_page = self.spider.parse_condition(fake_response_from_file('templates/empty_abdominal_aortic_aneurysm.html'))

        self._test_extracted_item(parsed_condition_page, expected_length, attributes)
        self._test_extracted_item_content(parsed_condition_page, valid_content)