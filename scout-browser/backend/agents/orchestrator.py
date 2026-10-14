from typing import Dict, Any, List
from agents.specialized_agents import specialized_agents
from agents.privacy_agent import privacy_agent

class OrchestratorAgent:
    def classify_and_plan(self, prompt: str) -> Dict[str, Any]:
        p = prompt.lower().strip()

        if "summarise this page" in p or "summarize this page" in p or "current page" in p:
            return {"intent": "page_summary", "agents": ["Page Understanding Agent", "Privacy Agent"]}

        if "paper" in p or "research" in p or "agentic ai" in p:
            return {"intent": "research", "agents": ["Research Agent", "Search Agent", "Privacy Agent"]}

        if "monitor" in p or "track" in p:
            return {"intent": "monitor_product", "agents": ["Shopping Agent", "Monitor Agent", "Privacy Agent"]}

        if "compare" in p and ("laptop" in p or "price" in p or "buy" in p):
            return {"intent": "shopping_compare", "agents": ["Shopping Agent", "Privacy Agent"]}

        if "hotel" in p or "book" in p:
            return {
                "intent": "search_and_book",
                "agents": ["Search Agent", "Shopping Agent", "Web Task Agent", "Privacy Agent"],
                "requires_confirmation": True,
            }

        if "sign me up" in p or "webinar" in p or "register" in p:
            return {
                "intent": "signup_with_alias",
                "agents": ["Web Task Agent", "Privacy Agent (Alias Shield)"],
                "requires_confirmation": True,
            }

        if "leak" in p or "who leaked" in p or "spam" in p:
            return {"intent": "catch_the_leaker", "agents": ["Privacy Agent (Catch the Leaker)"]}

        if "delete me" in p or "cleanup" in p or "apps i don't use" in p:
            return {
                "intent": "data_cleanup",
                "agents": ["Privacy Agent (Data Cleanup + Shared Deletion Map)"],
                "requires_confirmation": True,
            }

        return {"intent": "simple_search", "agents": ["Search Agent", "Privacy Agent"]}

    async def execute_workflow(
        self,
        prompt: str,
        current_url: str = None,
        open_tabs: List[str] = None,
        user_preferences: Dict[str, Any] = None,
        sample_accounts: List[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        plan = self.classify_and_plan(prompt)
        intent = plan["intent"]
        outputs = {}
        streaming_url = None
        requires_approval = plan.get("requires_confirmation", False)

        if intent == "page_summary":
            outputs["page"] = await specialized_agents.page_understanding_agent(prompt, current_url, open_tabs)

        elif intent == "research":
            outputs["search"] = await specialized_agents.search_agent(prompt)
            outputs["research"] = await specialized_agents.research_agent(prompt)

        elif intent == "shopping_compare":
            shop_res = await specialized_agents.shopping_agent(prompt, user_preferences)
            outputs["shopping"] = shop_res
            streaming_url = shop_res.get("streaming_url")

        elif intent == "monitor_product":
            shop_res = await specialized_agents.shopping_agent(prompt, user_preferences)
            mon_res = await specialized_agents.monitor_agent(target=prompt, duration_days=10)
            outputs["shopping"] = shop_res
            outputs["monitor"] = mon_res
            streaming_url = shop_res.get("streaming_url")

        elif intent == "search_and_book":
            outputs["search"] = await specialized_agents.search_agent(prompt)
            outputs["shopping"] = await specialized_agents.shopping_agent(prompt, user_preferences)
            task_res = await specialized_agents.web_task_agent(prompt, current_url)
            outputs["web_task"] = task_res
            streaming_url = task_res.get("streaming_url")

        elif intent == "signup_with_alias":
            task_res = await specialized_agents.web_task_agent(prompt, current_url)
            outputs["web_task"] = task_res
            streaming_url = task_res.get("streaming_url")

        elif intent == "catch_the_leaker":
            leak_report = await privacy_agent.inspect_inbound_email(
                alias_record={
                    "alias_email": "quickphoto-9b4k@myscout.id",
                    "assigned_app_name": "QuickPhoto Editor",
                    "assigned_domain": "quickphoto.io",
                    "known_partner_domains": [],
                    "created_at": "2026-01-19",
                },
                from_email="offers@instant-cash-loans24.biz",
                from_domain="instant-cash-loans24.biz",
                subject="Pre-approved Rs. 5,00,000 Instant Personal Loan!",
            )
            outputs["leak_investigation"] = leak_report

        elif intent == "data_cleanup":
            ranked = privacy_agent.rank_accounts_for_cleanup(sample_accounts or [])
            outputs["cleanup_ranking"] = ranked
            if ranked["recommended_for_deletion"]:
                top_target = ranked["recommended_for_deletion"][0]
                run1 = await privacy_agent.execute_deletion_run_1(top_target)
                outputs["deletion_run_1"] = run1
                streaming_url = run1.get("streaming_url")

        else:
            outputs["search"] = await specialized_agents.search_agent(prompt)

        return {
            "prompt": prompt,
            "intent": intent,
            "agents_invoked": plan["agents"],
            "requires_human_approval": requires_approval,
            "streaming_url": streaming_url,
            "outputs": outputs,
        }

orchestrator = OrchestratorAgent()
