import os
from dotenv import load_dotenv

load_dotenv()  # Load environment variables

import google.generativeai as genai

api_key = os.environ.get("GOOGLE_API_KEY")
if not api_key:
    print("Error: GOOGLE_API_KEY not found.")
    exit(1)

genai.configure(api_key=api_key)
model = genai.GenerativeModel('gemini-1.5-flash')

# Example long story (about 1000 characters)
long_text = """
At SolarTech Solutions, where unplanned downtime could mean thousands in lost revenue and broken customer trust, the pressure to deliver flawless software was relentless. Maya, the lead DevOps engineer, had seen it all—from last-minute production crashes to never-ending firefighting sprints.

But recently, everything was changing. Their DevOps pipeline now had a new teammate—not human, but an advanced Large Language Model (LLM) integrated directly into the workflow. This AI wasn’t just a tool; it was becoming a trusted partner, helping the team navigate the complex, high-stakes world of software delivery like never before.

One gray Tuesday morning, alerts started flooding the dashboard—automatic triggers that something mysterious was disrupting the cloud infrastructure. Usually, this would spark an all-hands-on-deck scramble, with engineers racing to diagnose logs, sift through hundreds of error messages, and patch configurations.

This time, Maya typed a quick question into the LLM-powered assistant:
"What could be causing the increased latency in our API gateway services?"

Within seconds, the LLM replied, analyzing recent deployment logs, matching error patterns with known issues, and referencing internal documentation:
"The spike correlates with the latest memory configuration changes applied last Friday. Similar incidents occurred three months ago due to suboptimal caching parameters."

Maya quickly tweaked the API gateway’s settings following the AI’s suggestion. The system’s performance stabilized before the customer support team even noticed any impact.

Relieved but curious, Maya decided to probe further. The LLM helped generate a detailed, blameless postmortem report by aggregating related commit diffs, identifying the exact lines of code that triggered the problem, and summarizing actions to prevent recurrence. The once arduous reporting task was now completed in minutes, freeing up the team to focus on innovation instead of paperwork.

Over the subsequent weeks, the LLM’s role expanded. It helped developers generate sophisticated deployment scripts from casual prompts such as:
"Create a Kubernetes rolling update to minimize downtime for the payment service."
The AI translated this into error-free YAML configurations, ready for execution.

Documentation—often overlooked in tight sprints—became effortlessly detailed as the LLM auto-generated changelogs, infrastructure diagrams, and security reviews with a single command.

Pull request reviews, once a bottleneck, sped up dramatically. The AI critically examined code for security vulnerabilities, compliance with best practices, and even suggested optimizations, all while learning the team’s coding style and preferences.

The real breakthrough was in collaboration. The AI was a conversational bridge between developers, testers, and operations personnel. Team members could ask complex questions like:

“How will this change affect our multi-region failover strategy?”

“Which services have dependencies on this database schema?”

The LLM answered seamlessly, integrating knowledge from both code and infrastructure documentation, eliminating silos and confusion.

As a result, SolarTech’s deployments evolved from chaotic, stressful episodes into predictable, confident releases. The team felt empowered, trusting both their own skills and the AI’s guidance. The balance of human intuition and machine precision created a new kind of DevOps harmony—one where creativity and reliability coexisted.

In board meetings, Maya proudly shared how integrating the LLM slashed incident resolution times by over 40% and improved deployment frequency without sacrificing stability. It was no longer just a backend tool but a strategic asset driving growth and innovation.

At SolarTech, the future of software delivery had arrived—a future where DevOps and AI walked hand in hand, transforming vast complex digital landscapes into symphonies of well-orchestrated code.
"""

prompt = f"Summarize the following story in 1-2 sentences with bullet points:\n{long_text}"
response = model.generate_content(prompt)

print("Summary:", response.text)
