"""
Slalom Capabilities Management System API

A FastAPI application that enables Slalom consultants to register their
capabilities and manage consulting expertise across the organization.
"""

from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import RedirectResponse
import os
from pathlib import Path

app = FastAPI(title="Slalom Capabilities Management API",
              description="API for managing consulting capabilities and consultant expertise")

# Mount the static files directory
current_dir = Path(__file__).parent
app.mount("/static", StaticFiles(directory=os.path.join(Path(__file__).parent,
          "static")), name="static")

# Competency Matrix definitions
competency_matrices = {
    "Cloud Architecture": {
        "Emerging": {
            "technical_excellence": {
                "domain_knowledge": "Understanding of basic cloud concepts (IaaS, PaaS, SaaS)",
                "tools_proficiency": "Learning AWS/Azure/GCP console and basic services",
                "architecture_design": "Designs simple single-service solutions with guidance",
                "best_practices": "Developing awareness of cloud security and cost optimization"
            },
            "client_delivery": {
                "engagement": "Participates in client meetings with senior guidance",
                "project_ownership": "Owns small tasks and components",
                "quality": "Delivers work that meets acceptance criteria with review",
                "communication": "Communicates progress and asks for help when needed"
            },
            "leadership": {
                "knowledge_sharing": "Documents learnings and shares with peers",
                "mentoring": "Learns from senior consultants",
                "community": "Participates in practice meetings",
                "growth": "Actively builds foundational cloud skills"
            }
        },
        "Proficient": {
            "technical_excellence": {
                "domain_knowledge": "Solid understanding of multi-cloud architectures and trade-offs",
                "tools_proficiency": "Proficient with IaC tools (Terraform, CloudFormation)",
                "architecture_design": "Designs scalable solutions considering availability and performance",
                "best_practices": "Applies cloud well-architected frameworks consistently"
            },
            "client_delivery": {
                "engagement": "Leads technical discussions with client stakeholders",
                "project_ownership": "Owns complete workstreams independently",
                "quality": "Delivers production-ready solutions with minimal oversight",
                "communication": "Proactively communicates risks and mitigation strategies"
            },
            "leadership": {
                "knowledge_sharing": "Presents at internal tech talks and creates practice content",
                "mentoring": "Mentors emerging cloud consultants",
                "community": "Contributes to practice standards and patterns",
                "growth": "Pursues cloud certifications and specializations"
            }
        },
        "Advanced": {
            "technical_excellence": {
                "domain_knowledge": "Deep expertise across multiple cloud platforms and hybrid solutions",
                "tools_proficiency": "Masters advanced automation and orchestration tools",
                "architecture_design": "Architects complex enterprise-scale cloud solutions",
                "best_practices": "Defines and evangelizes cloud best practices"
            },
            "client_delivery": {
                "engagement": "Trusted advisor to C-level executives on cloud strategy",
                "project_ownership": "Leads multiple complex engagements simultaneously",
                "quality": "Sets quality standards for cloud delivery across practice",
                "communication": "Influences client technology roadmaps and decisions"
            },
            "leadership": {
                "knowledge_sharing": "Publishes thought leadership and speaks at conferences",
                "mentoring": "Develops proficient consultants into senior practitioners",
                "community": "Shapes practice direction and capability offerings",
                "growth": "Pursues advanced certifications and drives innovation"
            }
        },
        "Expert": {
            "technical_excellence": {
                "domain_knowledge": "Industry-recognized authority on cloud architecture",
                "tools_proficiency": "Contributes to cloud tools and open-source projects",
                "architecture_design": "Pioneers innovative cloud architecture patterns",
                "best_practices": "Establishes industry standards and best practices"
            },
            "client_delivery": {
                "engagement": "Drives enterprise-wide cloud transformation strategies",
                "project_ownership": "Owns practice-level cloud delivery excellence",
                "quality": "Defines quality frameworks adopted organization-wide",
                "communication": "Thought leader influencing industry direction"
            },
            "leadership": {
                "knowledge_sharing": "Recognized external expert and keynote speaker",
                "mentoring": "Builds capability across the entire practice",
                "community": "Leads practice strategy and market positioning",
                "growth": "Sets vision for cloud practice evolution"
            }
        }
    }
}

# In-memory capabilities database
capabilities = {
    "Cloud Architecture": {
        "description": "Design and implement scalable cloud solutions using AWS, Azure, and GCP",
        "practice_area": "Technology",
        "skill_levels": ["Emerging", "Proficient", "Advanced", "Expert"],
        "certifications": ["AWS Solutions Architect", "Azure Architect Expert"],
        "industry_verticals": ["Healthcare", "Financial Services", "Retail"],
        "capacity": 40,  # hours per week available across team
        "consultants": ["alice.smith@slalom.com", "bob.johnson@slalom.com"],
        "has_competency_matrix": True
    },
    "Data Analytics": {
        "description": "Advanced data analysis, visualization, and machine learning solutions",
        "practice_area": "Technology", 
        "skill_levels": ["Emerging", "Proficient", "Advanced", "Expert"],
        "certifications": ["Tableau Desktop Specialist", "Power BI Expert", "Google Analytics"],
        "industry_verticals": ["Retail", "Healthcare", "Manufacturing"],
        "capacity": 35,
        "consultants": ["emma.davis@slalom.com", "sophia.wilson@slalom.com"],
        "has_competency_matrix": False
    },
    "DevOps Engineering": {
        "description": "CI/CD pipeline design, infrastructure automation, and containerization",
        "practice_area": "Technology",
        "skill_levels": ["Emerging", "Proficient", "Advanced", "Expert"], 
        "certifications": ["Docker Certified Associate", "Kubernetes Admin", "Jenkins Certified"],
        "industry_verticals": ["Technology", "Financial Services"],
        "capacity": 30,
        "consultants": ["john.brown@slalom.com", "olivia.taylor@slalom.com"],
        "has_competency_matrix": False
    },
    "Digital Strategy": {
        "description": "Digital transformation planning and strategic technology roadmaps",
        "practice_area": "Strategy",
        "skill_levels": ["Emerging", "Proficient", "Advanced", "Expert"],
        "certifications": ["Digital Transformation Certificate", "Agile Certified Practitioner"],
        "industry_verticals": ["Healthcare", "Financial Services", "Government"],
        "capacity": 25,
        "consultants": ["liam.anderson@slalom.com", "noah.martinez@slalom.com"],
        "has_competency_matrix": False
    },
    "Change Management": {
        "description": "Organizational change leadership and adoption strategies",
        "practice_area": "Operations",
        "skill_levels": ["Emerging", "Proficient", "Advanced", "Expert"],
        "certifications": ["Prosci Certified", "Lean Six Sigma Black Belt"],
        "industry_verticals": ["Healthcare", "Manufacturing", "Government"],
        "capacity": 20,
        "consultants": ["ava.garcia@slalom.com", "mia.rodriguez@slalom.com"],
        "has_competency_matrix": False
    },
    "UX/UI Design": {
        "description": "User experience design and digital product innovation",
        "practice_area": "Technology",
        "skill_levels": ["Emerging", "Proficient", "Advanced", "Expert"],
        "certifications": ["Adobe Certified Expert", "Google UX Design Certificate"],
        "industry_verticals": ["Retail", "Healthcare", "Technology"],
        "capacity": 30,
        "consultants": ["amelia.lee@slalom.com", "harper.white@slalom.com"],
        "has_competency_matrix": False
    },
    "Cybersecurity": {
        "description": "Information security strategy, risk assessment, and compliance",
        "practice_area": "Technology",
        "skill_levels": ["Emerging", "Proficient", "Advanced", "Expert"],
        "certifications": ["CISSP", "CISM", "CompTIA Security+"],
        "industry_verticals": ["Financial Services", "Healthcare", "Government"],
        "capacity": 25,
        "consultants": ["ella.clark@slalom.com", "scarlett.lewis@slalom.com"],
        "has_competency_matrix": False
    },
    "Business Intelligence": {
        "description": "Enterprise reporting, data warehousing, and business analytics",
        "practice_area": "Technology",
        "skill_levels": ["Emerging", "Proficient", "Advanced", "Expert"],
        "certifications": ["Microsoft BI Certification", "Qlik Sense Certified"],
        "industry_verticals": ["Retail", "Manufacturing", "Financial Services"],
        "capacity": 35,
        "consultants": ["james.walker@slalom.com", "benjamin.hall@slalom.com"],
        "has_competency_matrix": False
    },
    "Agile Coaching": {
        "description": "Agile transformation and team coaching for scaled delivery",
        "practice_area": "Operations",
        "skill_levels": ["Emerging", "Proficient", "Advanced", "Expert"],
        "certifications": ["Certified Scrum Master", "SAFe Agilist", "ICAgile Certified"],
        "industry_verticals": ["Technology", "Financial Services", "Healthcare"],
        "capacity": 20,
        "consultants": ["charlotte.young@slalom.com", "henry.king@slalom.com"],
        "has_competency_matrix": False
    }
}


@app.get("/")
def root():
    return RedirectResponse(url="/static/index.html")


@app.get("/capabilities")
def get_capabilities():
    return capabilities


@app.post("/capabilities/{capability_name}/register")
def register_for_capability(capability_name: str, email: str):
    """Register a consultant for a capability"""
    # Validate capability exists
    if capability_name not in capabilities:
        raise HTTPException(status_code=404, detail="Capability not found")

    # Get the specific capability
    capability = capabilities[capability_name]

    # Validate consultant is not already registered
    if email in capability["consultants"]:
        raise HTTPException(
            status_code=400,
            detail="Consultant is already registered for this capability"
        )

    # Add consultant
    capability["consultants"].append(email)
    return {"message": f"Registered {email} for {capability_name}"}


@app.delete("/capabilities/{capability_name}/unregister")
def unregister_from_capability(capability_name: str, email: str):
    """Unregister a consultant from a capability"""
    # Validate capability exists
    if capability_name not in capabilities:
        raise HTTPException(status_code=404, detail="Capability not found")

    # Get the specific capability
    capability = capabilities[capability_name]

    # Validate consultant is registered
    if email not in capability["consultants"]:
        raise HTTPException(
            status_code=400,
            detail="Consultant is not registered for this capability"
        )

    # Remove consultant
    capability["consultants"].remove(email)
    return {"message": f"Unregistered {email} from {capability_name}"}


@app.get("/capabilities/{capability_name}/competency-matrix")
def get_competency_matrix(capability_name: str):
    """Get the competency matrix for a specific capability"""
    # Validate capability exists
    if capability_name not in capabilities:
        raise HTTPException(status_code=404, detail="Capability not found")
    
    # Check if competency matrix exists for this capability
    if capability_name not in competency_matrices:
        raise HTTPException(
            status_code=404, 
            detail="Competency matrix not available for this capability yet"
        )
    
    return {
        "capability": capability_name,
        "matrix": competency_matrices[capability_name]
    }


@app.get("/competency-matrices")
def get_all_competency_matrices():
    """Get all available competency matrices"""
    return {
        "matrices": competency_matrices,
        "available_for": list(competency_matrices.keys())
    }
