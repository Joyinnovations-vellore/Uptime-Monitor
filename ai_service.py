import openai
import os
from typing import List, Dict, Any, Optional
import json
import logging
from dotenv import load_dotenv

load_dotenv()

class AIService:
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.openai_client = None
        self.setup_openai()
    
    def setup_openai(self):
        """Initialize OpenAI client"""
        api_key = os.getenv('OPENAI_API_KEY')
        if api_key:
            openai.api_key = api_key
            self.openai_client = openai.OpenAI(api_key=api_key)
        else:
            self.logger.warning("OpenAI API key not found. AI features will be limited.")
    
    async def enrich_data(self, data: List[Dict[str, Any]], prompt: str, model: str = "gpt-3.5-turbo") -> List[Dict[str, Any]]:
        """Enrich scraped data using AI"""
        if not self.openai_client:
            return self._mock_enrichment(data, prompt)
        
        try:
            enriched_data = []
            
            for item in data:
                try:
                    # Prepare the data for AI processing
                    data_context = self._prepare_data_context(item)
                    
                    # Create the AI prompt
                    ai_prompt = f"""
                    {prompt}
                    
                    Data to enrich:
                    {json.dumps(data_context, indent=2)}
                    
                    Please provide enriched information in JSON format. Focus on:
                    - Adding relevant metadata
                    - Extracting key insights
                    - Categorizing content
                    - Improving data quality
                    
                    Return only valid JSON without additional text.
                    """
                    
                    # Call OpenAI API
                    response = await self._call_openai(ai_prompt, model)
                    
                    # Parse AI response
                    ai_enrichment = self._parse_ai_response(response)
                    
                    # Merge original data with AI enrichment
                    enriched_item = {**item, **ai_enrichment}
                    enriched_data.append(enriched_item)
                    
                except Exception as e:
                    self.logger.error(f"Error enriching item: {str(e)}")
                    # Add original data with error flag
                    enriched_item = {**item, "ai_enrichment_error": str(e)}
                    enriched_data.append(enriched_item)
            
            return enriched_data
            
        except Exception as e:
            self.logger.error(f"Error in AI enrichment: {str(e)}")
            return data  # Return original data if AI fails
    
    async def _call_openai(self, prompt: str, model: str) -> str:
        """Call OpenAI API"""
        try:
            response = self.openai_client.chat.completions.create(
                model=model,
                messages=[
                    {"role": "system", "content": "You are a data enrichment assistant. Always respond with valid JSON."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=1000,
                temperature=0.3
            )
            return response.choices[0].message.content
        except Exception as e:
            self.logger.error(f"OpenAI API error: {str(e)}")
            raise e
    
    def _prepare_data_context(self, item: Dict[str, Any]) -> Dict[str, Any]:
        """Prepare data context for AI processing"""
        context = {}
        
        for key, value in item.items():
            if isinstance(value, dict) and 'text' in value:
                context[key] = value['text']
            elif isinstance(value, list):
                context[key] = [v.get('text', str(v)) if isinstance(v, dict) else str(v) for v in value]
            else:
                context[key] = str(value) if value is not None else ""
        
        return context
    
    def _parse_ai_response(self, response: str) -> Dict[str, Any]:
        """Parse AI response and extract JSON"""
        try:
            # Try to find JSON in the response
            start_idx = response.find('{')
            end_idx = response.rfind('}') + 1
            
            if start_idx != -1 and end_idx > start_idx:
                json_str = response[start_idx:end_idx]
                return json.loads(json_str)
            else:
                # If no JSON found, create a simple enrichment
                return {
                    "ai_summary": response.strip(),
                    "ai_processed": True
                }
        except json.JSONDecodeError:
            # If JSON parsing fails, create a simple enrichment
            return {
                "ai_summary": response.strip(),
                "ai_processed": True,
                "ai_parse_error": "Could not parse AI response as JSON"
            }
    
    def _mock_enrichment(self, data: List[Dict[str, Any]], prompt: str) -> List[Dict[str, Any]]:
        """Mock enrichment when AI is not available"""
        enriched_data = []
        
        for item in data:
            mock_enrichment = {
                "ai_summary": f"Mock enrichment for: {prompt[:50]}...",
                "ai_processed": False,
                "ai_mock": True,
                "ai_timestamp": "2024-01-01T00:00:00Z"
            }
            enriched_item = {**item, **mock_enrichment}
            enriched_data.append(enriched_item)
        
        return enriched_data
    
    async def generate_insights(self, data: List[Dict[str, Any]], analysis_type: str = "general") -> Dict[str, Any]:
        """Generate insights from scraped data"""
        if not self.openai_client:
            return self._mock_insights(data, analysis_type)
        
        try:
            # Prepare data summary
            data_summary = self._create_data_summary(data)
            
            prompt = f"""
            Analyze the following scraped data and provide insights:
            
            Analysis Type: {analysis_type}
            Data Summary: {json.dumps(data_summary, indent=2)}
            
            Please provide:
            1. Key trends and patterns
            2. Data quality assessment
            3. Recommendations for improvement
            4. Statistical summary
            
            Return as JSON with the following structure:
            {{
                "trends": ["trend1", "trend2"],
                "quality_score": 0.85,
                "recommendations": ["rec1", "rec2"],
                "statistics": {{"total_items": 100, "unique_domains": 5}}
            }}
            """
            
            response = await self._call_openai(prompt, "gpt-3.5-turbo")
            insights = self._parse_ai_response(response)
            
            return {
                "analysis_type": analysis_type,
                "insights": insights,
                "data_count": len(data),
                "generated_at": "2024-01-01T00:00:00Z"
            }
            
        except Exception as e:
            self.logger.error(f"Error generating insights: {str(e)}")
            return self._mock_insights(data, analysis_type)
    
    def _create_data_summary(self, data: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Create a summary of the data for AI analysis"""
        if not data:
            return {"empty": True}
        
        summary = {
            "total_items": len(data),
            "sample_data": data[:3] if len(data) > 3 else data,
            "fields": list(data[0].keys()) if data else [],
            "urls": [item.get('url', 'unknown') for item in data if 'url' in item]
        }
        
        return summary
    
    def _mock_insights(self, data: List[Dict[str, Any]], analysis_type: str) -> Dict[str, Any]:
        """Mock insights when AI is not available"""
        return {
            "analysis_type": analysis_type,
            "insights": {
                "trends": ["Mock trend 1", "Mock trend 2"],
                "quality_score": 0.75,
                "recommendations": ["Mock recommendation 1", "Mock recommendation 2"],
                "statistics": {
                    "total_items": len(data),
                    "unique_domains": len(set(item.get('url', '') for item in data))
                }
            },
            "data_count": len(data),
            "generated_at": "2024-01-01T00:00:00Z",
            "mock": True
        }
    
    async def validate_data_quality(self, data: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Validate data quality using AI"""
        if not self.openai_client:
            return self._mock_quality_validation(data)
        
        try:
            data_sample = data[:5] if len(data) > 5 else data
            
            prompt = f"""
            Analyze the quality of this scraped data:
            
            {json.dumps(data_sample, indent=2)}
            
            Provide quality assessment in JSON format:
            {{
                "overall_score": 0.85,
                "completeness": 0.90,
                "accuracy": 0.80,
                "consistency": 0.85,
                "issues": ["issue1", "issue2"],
                "recommendations": ["rec1", "rec2"]
            }}
            """
            
            response = await self._call_openai(prompt, "gpt-3.5-turbo")
            quality_assessment = self._parse_ai_response(response)
            
            return {
                "data_count": len(data),
                "assessment": quality_assessment,
                "validated_at": "2024-01-01T00:00:00Z"
            }
            
        except Exception as e:
            self.logger.error(f"Error validating data quality: {str(e)}")
            return self._mock_quality_validation(data)
    
    def _mock_quality_validation(self, data: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Mock quality validation when AI is not available"""
        return {
            "data_count": len(data),
            "assessment": {
                "overall_score": 0.75,
                "completeness": 0.80,
                "accuracy": 0.70,
                "consistency": 0.75,
                "issues": ["Mock issue 1", "Mock issue 2"],
                "recommendations": ["Mock recommendation 1", "Mock recommendation 2"]
            },
            "validated_at": "2024-01-01T00:00:00Z",
            "mock": True
        }
