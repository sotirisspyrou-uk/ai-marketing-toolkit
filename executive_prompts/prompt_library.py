"""
Executive AI Prompt Library

C-suite focused prompts for strategic decision-making.
Delivers faster strategic analysis and data-driven insights.
"""

from typing import Dict, List, Optional, Union, Tuple
from dataclasses import dataclass
from enum import Enum
import json
from datetime import datetime

class PromptCategory(Enum):
    """Categories of executive prompts."""
    MARKET_ANALYSIS = "market_analysis"
    COMPETITIVE_INTELLIGENCE = "competitive_intelligence"
    STRATEGIC_PLANNING = "strategic_planning"
    RISK_ASSESSMENT = "risk_assessment"
    PERFORMANCE_ANALYSIS = "performance_analysis"
    INVESTOR_RELATIONS = "investor_relations"
    CRISIS_MANAGEMENT = "crisis_management"
    INNOVATION_STRATEGY = "innovation_strategy"

class ExecutiveLevel(Enum):
    """Executive levels for tailored prompts."""
    CEO = "ceo"
    CMO = "cmo"
    CFO = "cfo"
    CTO = "cto"
    VP_MARKETING = "vp_marketing"
    VP_SALES = "vp_sales"
    BOARD_MEMBER = "board_member"

@dataclass
class PromptTemplate:
    """Executive prompt template with metadata."""
    name: str
    category: PromptCategory
    executive_level: List[ExecutiveLevel]
    template: str
    variables: List[str]
    expected_outcome: str
    use_case: str
    business_impact: str
    time_to_insight: str

class ExecutivePromptLibrary:
    """
    Curated library of AI prompts for executive decision-making.
    
    Features:
    - C-suite focused strategic prompts
    - Market intelligence templates
    - Competitive analysis frameworks
    - Risk assessment protocols
    - Board presentation generators
    """
    
    def __init__(self):
        """Initialize the executive prompt library."""
        self.prompts = self._initialize_prompt_library()
    
    def _initialize_prompt_library(self) -> Dict[str, PromptTemplate]:
        """Initialize the comprehensive prompt library."""
        return {
            "market_opportunity_analysis": PromptTemplate(
                name="Market Opportunity Analysis",
                category=PromptCategory.MARKET_ANALYSIS,
                executive_level=[ExecutiveLevel.CEO, ExecutiveLevel.CMO, ExecutiveLevel.VP_MARKETING],
                template="""
Analyze the market opportunity for {product_category} in {target_market} region.

Consider the following factors:
- Total Addressable Market (TAM) size and growth projections
- Current market penetration and saturation levels
- Key customer segments and their pain points
- Regulatory environment and compliance requirements
- Technology trends affecting the market
- Economic indicators and their impact

Provide a structured analysis including:
1. Market size and growth potential ($USD and %)
2. Competitive landscape overview (top 5 players)
3. Key opportunities and threats
4. Recommended market entry strategy
5. Investment requirements and ROI projections
6. Timeline for market penetration

Format the response as an executive summary suitable for board presentation.
                """.strip(),
                variables=["product_category", "target_market"],
                expected_outcome="Comprehensive market opportunity assessment with actionable recommendations",
                use_case="New market entry decisions, investment planning, strategic positioning",
                business_impact="Informed market entry decisions, reduced investment risk, accelerated growth",
                time_to_insight="15 minutes"
            ),
            
            "competitive_positioning_analysis": PromptTemplate(
                name="Competitive Positioning Analysis",
                category=PromptCategory.COMPETITIVE_INTELLIGENCE,
                executive_level=[ExecutiveLevel.CEO, ExecutiveLevel.CMO, ExecutiveLevel.VP_MARKETING],
                template="""
Conduct a comprehensive competitive positioning analysis for {company_name} against {competitor_list}.

Analysis Framework:
1. Market Position Assessment
   - Market share comparison
   - Brand perception and positioning
   - Customer loyalty metrics
   - Pricing strategy analysis

2. Product/Service Comparison
   - Feature and capability matrix
   - Quality and performance benchmarks
   - Innovation pipeline comparison
   - Customer satisfaction scores

3. Strategic Advantages Analysis
   - Core competencies and differentiators
   - Resource and capability gaps
   - Operational efficiency comparison
   - Technology and innovation leadership

4. Threat Assessment
   - Competitive threats and vulnerabilities
   - Market disruption risks
   - New entrant possibilities
   - Substitute product threats

Deliverable:
- Executive summary with key findings
- Competitive positioning map
- Strategic recommendations for maintaining/improving position
- Action plan with priorities and timelines

Focus on actionable insights that drive competitive advantage.
                """.strip(),
                variables=["company_name", "competitor_list"],
                expected_outcome="Detailed competitive analysis with strategic positioning recommendations",
                use_case="Strategic planning, competitive response, market positioning",
                business_impact="Enhanced competitive advantage, better strategic positioning, informed decision-making",
                time_to_insight="20 minutes"
            ),
            
            "risk_assessment_framework": PromptTemplate(
                name="Strategic Risk Assessment",
                category=PromptCategory.RISK_ASSESSMENT,
                executive_level=[ExecutiveLevel.CEO, ExecutiveLevel.CFO, ExecutiveLevel.BOARD_MEMBER],
                template="""
Perform a comprehensive risk assessment for {business_initiative} considering {time_horizon} timeframe.

Risk Assessment Categories:

1. Market Risks
   - Demand fluctuation and market volatility
   - Competitive response and market share erosion
   - Economic downturn and recession impact
   - Customer behavior changes

2. Operational Risks
   - Supply chain disruptions
   - Technology failures and cybersecurity threats
   - Key personnel dependencies
   - Quality and compliance issues

3. Financial Risks
   - Cash flow and liquidity constraints
   - Currency and interest rate fluctuations
   - Credit and counterparty risks
   - Investment and capital allocation risks

4. Strategic Risks
   - Technology disruption and obsolescence
   - Regulatory changes and compliance costs
   - Reputation and brand damage
   - M&A integration challenges

For each risk:
- Probability assessment (Low/Medium/High)
- Impact severity (1-5 scale)
- Risk score (Probability × Impact)
- Mitigation strategies
- Contingency plans
- Monitoring indicators

Provide executive summary with:
- Top 5 critical risks requiring immediate attention
- Risk mitigation budget recommendations
- Key performance indicators for monitoring
- Recommended governance and oversight structure
                """.strip(),
                variables=["business_initiative", "time_horizon"],
                expected_outcome="Comprehensive risk assessment with mitigation strategies and monitoring framework",
                use_case="Strategic planning, investment decisions, board reporting, compliance",
                business_impact="Reduced business risks, improved decision-making, enhanced stakeholder confidence",
                time_to_insight="25 minutes"
            ),
            
            "performance_optimization_analysis": PromptTemplate(
                name="Business Performance Optimization",
                category=PromptCategory.PERFORMANCE_ANALYSIS,
                executive_level=[ExecutiveLevel.CEO, ExecutiveLevel.CFO, ExecutiveLevel.CMO],
                template="""
Analyze current business performance for {business_unit} and identify optimization opportunities.

Performance Analysis Framework:

1. Financial Performance Review
   - Revenue growth trends and drivers
   - Profitability analysis (gross, operating, net margins)
   - Cash flow generation and working capital efficiency
   - ROI and ROIC analysis by business segment

2. Operational Efficiency Assessment
   - Key productivity metrics and benchmarks
   - Process optimization opportunities
   - Technology leverage and automation potential
   - Resource allocation effectiveness

3. Market Performance Evaluation
   - Market share trends and competitive position
   - Customer acquisition and retention metrics
   - Brand strength and market perception
   - Channel effectiveness and optimization

4. Strategic Alignment Check
   - Performance against strategic objectives
   - Initiative effectiveness and ROI
   - Resource allocation optimization
   - Portfolio performance and prioritization

Deliverables:
1. Performance dashboard with key metrics
2. Gap analysis against industry benchmarks
3. Top 10 optimization opportunities ranked by impact/effort
4. Implementation roadmap with quick wins and long-term initiatives
5. Investment requirements and expected returns
6. Performance tracking and monitoring framework

Focus on actionable recommendations with clear business impact quantification.
                """.strip(),
                variables=["business_unit"],
                expected_outcome="Performance optimization roadmap with prioritized initiatives and ROI projections",
                use_case="Strategic planning, operational improvement, resource optimization",
                business_impact="Improved operational efficiency, increased profitability, enhanced competitive position",
                time_to_insight="30 minutes"
            ),
            
            "investor_presentation_generator": PromptTemplate(
                name="Investor Presentation Content",
                category=PromptCategory.INVESTOR_RELATIONS,
                executive_level=[ExecutiveLevel.CEO, ExecutiveLevel.CFO],
                template="""
Generate compelling investor presentation content for {presentation_type} focusing on {key_themes}.

Presentation Structure:

1. Executive Summary
   - Company overview and value proposition
   - Key financial highlights and achievements
   - Strategic priorities and growth drivers
   - Investment thesis and value creation story

2. Business Performance
   - Financial results and key metrics
   - Operational achievements and milestones
   - Market position and competitive advantages
   - Customer and product momentum

3. Strategic Outlook
   - Market opportunities and growth potential
   - Strategic initiatives and investments
   - Innovation pipeline and competitive moats
   - Long-term financial targets and projections

4. Financial Analysis
   - Revenue growth and profitability trends
   - Capital allocation and returns
   - Cash generation and balance sheet strength
   - Valuation metrics and peer comparisons

5. Risk Management
   - Key risks and mitigation strategies
   - Scenario analysis and stress testing
   - Governance and compliance framework
   - Stakeholder engagement approach

Content Requirements:
- Clear and compelling narrative with data support
- Visual elements suggestions (charts, graphs, infographics)
- Key messages for each section
- Q&A preparation points
- Call-to-action and next steps

Tone: Professional, confident, data-driven, forward-looking
Audience: Institutional investors, analysts, stakeholders
Duration: {presentation_duration} minutes
                """.strip(),
                variables=["presentation_type", "key_themes", "presentation_duration"],
                expected_outcome="Complete investor presentation content with supporting materials",
                use_case="Investor meetings, earnings calls, IPO roadshows, strategic updates",
                business_impact="Enhanced investor confidence, improved valuation, stronger stakeholder relationships",
                time_to_insight="45 minutes"
            ),
            
            "crisis_management_response": PromptTemplate(
                name="Crisis Management Response",
                category=PromptCategory.CRISIS_MANAGEMENT,
                executive_level=[ExecutiveLevel.CEO, ExecutiveLevel.CMO, ExecutiveLevel.BOARD_MEMBER],
                template="""
Develop a comprehensive crisis management response for {crisis_type} affecting {affected_areas}.

Crisis Response Framework:

1. Immediate Assessment
   - Situation analysis and impact evaluation
   - Stakeholder mapping and communication priorities
   - Legal and regulatory implications
   - Media and public perception risks

2. Response Strategy
   - Key messages and communication approach
   - Stakeholder-specific response plans
   - Timeline and action priorities
   - Resource allocation and team assignments

3. Communication Plan
   - Internal communication (employees, board, shareholders)
   - External communication (customers, media, regulators)
   - Social media and digital response strategy
   - Crisis spokesperson selection and preparation

4. Operational Response
   - Business continuity measures
   - Customer service and support protocols
   - Supply chain and partner communications
   - Financial and insurance considerations

5. Recovery and Learning
   - Post-crisis evaluation and lessons learned
   - Process improvements and prevention measures
   - Reputation repair and rebuilding strategy
   - Long-term monitoring and follow-up

Deliverables:
- Crisis response playbook
- Communication templates and key messages
- Decision-making framework and escalation procedures
- Monitoring dashboard and success metrics
- Post-crisis analysis and improvement plan

Priority Focus:
- Stakeholder safety and protection
- Business continuity and operations
- Reputation and brand protection
- Legal and regulatory compliance
- Long-term relationship preservation
                """.strip(),
                variables=["crisis_type", "affected_areas"],
                expected_outcome="Comprehensive crisis management plan with communication strategy and operational response",
                use_case="Crisis response, reputation management, stakeholder communication",
                business_impact="Minimized crisis impact, protected reputation, maintained stakeholder confidence",
                time_to_insight="60 minutes"
            ),
            
            "innovation_strategy_development": PromptTemplate(
                name="Innovation Strategy Development",
                category=PromptCategory.INNOVATION_STRATEGY,
                executive_level=[ExecutiveLevel.CEO, ExecutiveLevel.CTO, ExecutiveLevel.VP_MARKETING],
                template="""
Develop a comprehensive innovation strategy for {organization} focusing on {innovation_focus_areas}.

Innovation Strategy Framework:

1. Innovation Landscape Analysis
   - Technology trends and emerging opportunities
   - Competitive innovation patterns and benchmarks
   - Customer needs evolution and unmet demands
   - Regulatory and market environment changes

2. Innovation Capabilities Assessment
   - Current innovation assets and competencies
   - R&D capabilities and infrastructure
   - Talent and organizational readiness
   - Partnership and ecosystem relationships

3. Strategic Innovation Priorities
   - Core innovation themes and focus areas
   - Innovation portfolio balance (core/adjacent/transformational)
   - Resource allocation and investment priorities
   - Timeline and milestone planning

4. Innovation Operating Model
   - Organizational structure and governance
   - Innovation processes and methodologies
   - Performance metrics and KPIs
   - Risk management and decision-making frameworks

5. Implementation Roadmap
   - Phase-gate approach with key milestones
   - Resource requirements and budget allocation
   - Partnership and collaboration strategy
   - Change management and cultural transformation

Innovation Investment Areas:
- Technology and digital transformation
- Product and service innovation
- Business model innovation
- Process and operational innovation
- Sustainability and ESG innovation

Success Metrics:
- Innovation pipeline strength and conversion
- Time-to-market and commercialization success
- Revenue from new products/services
- Patent portfolio and IP value creation
- Innovation ROI and value creation

Deliverables:
- Innovation strategy document
- Innovation roadmap and portfolio
- Governance framework and processes
- Investment plan and resource allocation
- Performance dashboard and monitoring system
                """.strip(),
                variables=["organization", "innovation_focus_areas"],
                expected_outcome="Comprehensive innovation strategy with implementation roadmap and success metrics",
                use_case="Strategic planning, R&D investment, technology roadmapping, competitive differentiation",
                business_impact="Enhanced innovation capabilities, accelerated growth, competitive advantage",
                time_to_insight="40 minutes"
            )
        }
    
    def get_prompt(self, prompt_name: str, variables: Dict[str, str]) -> str:
        """
        Get a formatted prompt with variables filled in.
        
        Args:
            prompt_name: Name of the prompt template
            variables: Dictionary of variable values
            
        Returns:
            Formatted prompt ready for AI processing
        """
        if prompt_name not in self.prompts:
            raise ValueError(f"Prompt '{prompt_name}' not found in library")
        
        template = self.prompts[prompt_name]
        formatted_prompt = template.template
        
        for var_name, var_value in variables.items():
            placeholder = "{" + var_name + "}"
            formatted_prompt = formatted_prompt.replace(placeholder, var_value)
        
        return formatted_prompt
    
    def list_prompts_by_category(self, category: PromptCategory) -> List[str]:
        """
        List all prompts in a specific category.
        
        Args:
            category: Prompt category to filter by
            
        Returns:
            List of prompt names in the category
        """
        return [
            name for name, template in self.prompts.items()
            if template.category == category
        ]
    
    def list_prompts_by_executive_level(self, executive_level: ExecutiveLevel) -> List[str]:
        """
        List prompts suitable for a specific executive level.
        
        Args:
            executive_level: Executive level to filter by
            
        Returns:
            List of prompt names suitable for the executive level
        """
        return [
            name for name, template in self.prompts.items()
            if executive_level in template.executive_level
        ]
    
    def get_prompt_metadata(self, prompt_name: str) -> Dict[str, str]:
        """
        Get metadata for a specific prompt.
        
        Args:
            prompt_name: Name of the prompt
            
        Returns:
            Dictionary containing prompt metadata
        """
        if prompt_name not in self.prompts:
            raise ValueError(f"Prompt '{prompt_name}' not found in library")
        
        template = self.prompts[prompt_name]
        return {
            'name': template.name,
            'category': template.category.value,
            'executive_levels': [level.value for level in template.executive_level],
            'variables': template.variables,
            'expected_outcome': template.expected_outcome,
            'use_case': template.use_case,
            'business_impact': template.business_impact,
            'time_to_insight': template.time_to_insight
        }
    
    def search_prompts(self, keyword: str) -> List[str]:
        """
        Search prompts by keyword in name, use case, or business impact.
        
        Args:
            keyword: Search keyword
            
        Returns:
            List of matching prompt names
        """
        keyword_lower = keyword.lower()
        matching_prompts = []
        
        for name, template in self.prompts.items():
            search_text = f"{template.name} {template.use_case} {template.business_impact}".lower()
            if keyword_lower in search_text:
                matching_prompts.append(name)
        
        return matching_prompts
    
    def generate_prompt_catalog(self) -> str:
        """
        Generate a comprehensive catalog of all available prompts.
        
        Returns:
            Formatted catalog string
        """
        catalog = "EXECUTIVE AI PROMPT LIBRARY CATALOG\n"
        catalog += "=" * 50 + "\n\n"
        
        # Group by category
        for category in PromptCategory:
            category_prompts = self.list_prompts_by_category(category)
            if category_prompts:
                catalog += f"{category.value.replace('_', ' ').title()}\n"
                catalog += "-" * 30 + "\n"
                
                for prompt_name in category_prompts:
                    template = self.prompts[prompt_name]
                    catalog += f"\n{template.name}\n"
                    catalog += f"Executive Levels: {', '.join([level.value.upper() for level in template.executive_level])}\n"
                    catalog += f"Use Case: {template.use_case}\n"
                    catalog += f"Business Impact: {template.business_impact}\n"
                    catalog += f"Time to Insight: {template.time_to_insight}\n"
                    catalog += f"Variables: {', '.join(template.variables)}\n"
                    catalog += "\n"
                
                catalog += "\n"
        
        return catalog
    
    def create_custom_prompt(self, 
                           name: str,
                           category: PromptCategory,
                           executive_level: List[ExecutiveLevel],
                           template: str,
                           variables: List[str],
                           expected_outcome: str,
                           use_case: str,
                           business_impact: str,
                           time_to_insight: str) -> str:
        """
        Create and add a custom prompt to the library.
        
        Args:
            name: Unique name for the prompt
            category: Prompt category
            executive_level: List of suitable executive levels
            template: Prompt template with variable placeholders
            variables: List of variable names used in template
            expected_outcome: Expected outcome description
            use_case: Use case description
            business_impact: Business impact description
            time_to_insight: Expected time to generate insights
            
        Returns:
            Success message
        """
        prompt_key = name.lower().replace(' ', '_')
        
        if prompt_key in self.prompts:
            raise ValueError(f"Prompt with name '{name}' already exists")
        
        custom_prompt = PromptTemplate(
            name=name,
            category=category,
            executive_level=executive_level,
            template=template,
            variables=variables,
            expected_outcome=expected_outcome,
            use_case=use_case,
            business_impact=business_impact,
            time_to_insight=time_to_insight
        )
        
        self.prompts[prompt_key] = custom_prompt
        return f"Custom prompt '{name}' added successfully to the library"
    
    def export_prompts_json(self) -> str:
        """
        Export all prompts to JSON format.
        
        Returns:
            JSON string containing all prompts
        """
        export_data = {}
        
        for name, template in self.prompts.items():
            export_data[name] = {
                'name': template.name,
                'category': template.category.value,
                'executive_level': [level.value for level in template.executive_level],
                'template': template.template,
                'variables': template.variables,
                'expected_outcome': template.expected_outcome,
                'use_case': template.use_case,
                'business_impact': template.business_impact,
                'time_to_insight': template.time_to_insight
            }
        
        return json.dumps(export_data, indent=2)
    
    def get_recommended_prompts_for_role(self, role: ExecutiveLevel) -> Dict[str, List[str]]:
        """
        Get recommended prompts organized by category for a specific executive role.
        
        Args:
            role: Executive level
            
        Returns:
            Dictionary with categories as keys and lists of prompt names as values
        """
        role_prompts = self.list_prompts_by_executive_level(role)
        categorized_prompts = {}
        
        for prompt_name in role_prompts:
            template = self.prompts[prompt_name]
            category_name = template.category.value
            
            if category_name not in categorized_prompts:
                categorized_prompts[category_name] = []
            
            categorized_prompts[category_name].append(prompt_name)
        
        return categorized_prompts


def main():
    """Example usage demonstration."""
    library = ExecutivePromptLibrary()
    
    # Example 1: Get a market analysis prompt
    variables = {
        "product_category": "AI-powered marketing tools",
        "target_market": "North American enterprise"
    }
    
    prompt = library.get_prompt("market_opportunity_analysis", variables)
    print("Market Analysis Prompt:")
    print("-" * 50)
    print(prompt)
    print("\n")
    
    # Example 2: List prompts for CMO
    cmo_prompts = library.get_recommended_prompts_for_role(ExecutiveLevel.CMO)
    print("Recommended Prompts for CMO:")
    print("-" * 30)
    for category, prompts in cmo_prompts.items():
        print(f"{category.replace('_', ' ').title()}:")
        for prompt in prompts:
            print(f"  - {library.prompts[prompt].name}")
    print("\n")
    
    # Example 3: Search prompts
    risk_prompts = library.search_prompts("risk")
    print(f"Risk-related prompts: {risk_prompts}")
    
    # Example 4: Generate catalog
    catalog = library.generate_prompt_catalog()
    print("\nPrompt Catalog Preview (first 500 chars):")
    print(catalog[:500] + "...")


if __name__ == "__main__":
    main()