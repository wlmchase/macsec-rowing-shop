# As an attacker
I want to gain unauthorized access  
I want to gain admin priviledges  
I want to gain sensitive data from the DB  
I want to redirect traffic to my malicious Site/API  
I want to inject code when making purchases to gain financially  
I want to inject malicious data into the DB  
I want to make the site unavailable or slow - DoS  

# As a developer
I want to maintain customer trust by keeping their data confidential in transit and at rest  
I want to maintain data integrity  
I want to maintain service and data availability  

## Login Page Defense strategies
force strong passwords (12 chars, number, lower, upper, special char)  
Check for known weak passwords  

## Injection Defenses
input sanitization  
structured queries with expected variables  

## DoS Defenses
rate limits  
requests/min limit  

## XSS Defenses
robust cross origin configs  

## Data Confidentiality & Integrity
Encryption & hashing  
DB noise for privacy  

# Information gathering 
Logs  