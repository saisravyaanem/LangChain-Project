import os
import requests
from dotenv import load_dotenv


load_dotenv()



def scrape_linkedin_profile(linkedin_profile_url: str, mock: bool=False):
    """scrape information from LinkedIn profiles,
    Manually scrape the information from the LinkedIn profile"""
    
    if mock:
        linkedin_profile_url="https://gist.githubusercontent.com/saisravyaanem/6467acb8b590fd6cd88cbcfe876b7a1f/raw/2cc6ab27b0498c0a679fcb0e23036d57a7b9bd8e/sai-sravya-scrapin.json"
        response=requests.get(
            linkedin_profile_url,
            timeout=10,
        )
    else:
        api_endpoint="https://api.scrapin.io/enrichment/profile"
        params={
            "apikey":os.environ["SCRAPIN_API_KEY"],
            "linkedInUrl": linkedin_profile_url
        }
        
        response=requests.get(
            api_endpoint,
            params=params,
            timeout=10,
        )
        
    data=response.json().get("person")
        
    data={
        k:v
        for k,v in data.items()
        if v not in ([],"","",None)
        and k not in ["certifications"]
        }
        
    return data
        
    
    
    
if __name__=="__main__":
    print(
        scrape_linkedin_profile(linkedin_profile_url="https://www.linkedin.com/in/sai-sravya-anem-1bb98b217/",mock=True
                                  ))    
    