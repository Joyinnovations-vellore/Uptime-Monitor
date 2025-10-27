# import pandas as pd  # Temporarily disabled due to installation issues
import json
import os
import aiofiles
from typing import List, Dict, Any, Optional
import logging
from datetime import datetime
import uuid

class DataProcessor:
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.data_dir = "data"
        self.templates_dir = "templates"
        self.ensure_directories()
    
    def ensure_directories(self):
        """Create necessary directories if they don't exist"""
        os.makedirs(self.data_dir, exist_ok=True)
        os.makedirs(self.templates_dir, exist_ok=True)
    
    async def export_to_excel(self, data: List[Dict[str, Any]], filename: Optional[str] = None) -> str:
        """Export data to Excel format (simplified without pandas)"""
        try:
            if not data:
                raise ValueError("No data to export")
            
            # Generate filename if not provided
            if not filename:
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                filename = f"scraped_data_{timestamp}.xlsx"
            
            # Ensure .xlsx extension
            if not filename.endswith('.xlsx'):
                filename += '.xlsx'
            
            file_path = os.path.join(self.data_dir, filename)
            
            # For now, export as JSON since pandas is not available
            # In production, you would use openpyxl directly or install pandas
            json_file = file_path.replace('.xlsx', '.json')
            await self.export_to_json(data, os.path.basename(json_file))
            
            self.logger.info(f"Data exported as JSON (Excel not available): {json_file}")
            return json_file
            
        except Exception as e:
            self.logger.error(f"Error exporting data: {str(e)}")
            raise e
    
    async def export_to_json(self, data: List[Dict[str, Any]], filename: Optional[str] = None) -> str:
        """Export data to JSON format"""
        try:
            if not data:
                raise ValueError("No data to export")
            
            # Generate filename if not provided
            if not filename:
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                filename = f"scraped_data_{timestamp}.json"
            
            # Ensure .json extension
            if not filename.endswith('.json'):
                filename += '.json'
            
            file_path = os.path.join(self.data_dir, filename)
            
            # Prepare export data with metadata
            export_data = {
                "metadata": {
                    "exported_at": datetime.now().isoformat(),
                    "total_records": len(data),
                    "export_format": "json",
                    "version": "1.0"
                },
                "data": data
            }
            
            # Write JSON file
            async with aiofiles.open(file_path, 'w', encoding='utf-8') as f:
                await f.write(json.dumps(export_data, indent=2, ensure_ascii=False))
            
            self.logger.info(f"JSON file exported successfully: {file_path}")
            return file_path
            
        except Exception as e:
            self.logger.error(f"Error exporting to JSON: {str(e)}")
            raise e
    
    def _prepare_dataframe(self, data: List[Dict[str, Any]]):
        """Prepare DataFrame from scraped data"""
        try:
            # Flatten nested data for better Excel compatibility
            flattened_data = []
            
            for item in data:
                flattened_item = {}
                
                for key, value in item.items():
                    if isinstance(value, dict):
                        # Handle nested objects
                        for nested_key, nested_value in value.items():
                            if isinstance(nested_value, (str, int, float, bool)):
                                flattened_item[f"{key}_{nested_key}"] = nested_value
                            else:
                                flattened_item[f"{key}_{nested_key}"] = str(nested_value)
                    elif isinstance(value, list):
                        # Handle lists
                        if value and isinstance(value[0], dict):
                            # List of objects - create columns for each object
                            for i, list_item in enumerate(value):
                                if isinstance(list_item, dict):
                                    for nested_key, nested_value in list_item.items():
                                        flattened_item[f"{key}_{i}_{nested_key}"] = nested_value
                        else:
                            # Simple list - join as string
                            flattened_item[key] = " | ".join(str(v) for v in value)
                    else:
                        flattened_item[key] = value
                
                flattened_data.append(flattened_item)
            
            return flattened_data
            
        except Exception as e:
            self.logger.error(f"Error preparing DataFrame: {str(e)}")
            # Return basic DataFrame if flattening fails
            return data
    
    def _create_summary_dataframe(self, data: List[Dict[str, Any]]):
        """Create summary DataFrame"""
        try:
            summary_data = []
            
            # Basic statistics
            summary_data.append({
                "Metric": "Total Records",
                "Value": len(data),
                "Description": "Total number of scraped records"
            })
            
            # URL statistics
            urls = [item.get('url', '') for item in data if 'url' in item]
            unique_urls = len(set(urls))
            summary_data.append({
                "Metric": "Unique URLs",
                "Value": unique_urls,
                "Description": "Number of unique URLs scraped"
            })
            
            # Field statistics
            if data:
                all_fields = set()
                for item in data:
                    all_fields.update(item.keys())
                
                summary_data.append({
                    "Metric": "Total Fields",
                    "Value": len(all_fields),
                    "Description": "Number of different fields extracted"
                })
            
            # Success rate
            successful_items = len([item for item in data if item.get('status') != 'error'])
            success_rate = (successful_items / len(data)) * 100 if data else 0
            summary_data.append({
                "Metric": "Success Rate",
                "Value": f"{success_rate:.1f}%",
                "Description": "Percentage of successfully scraped items"
            })
            
            return summary_data
            
        except Exception as e:
            self.logger.error(f"Error creating summary DataFrame: {str(e)}")
            return [{"Metric": "Error", "Value": str(e), "Description": "Error creating summary"}]
    
    def _create_statistics_dataframe(self, data: List[Dict[str, Any]]):
        """Create statistics DataFrame"""
        try:
            stats_data = []
            
            # Field completion statistics
            if data:
                field_stats = {}
                for item in data:
                    for field, value in item.items():
                        if field not in field_stats:
                            field_stats[field] = {"total": 0, "filled": 0}
                        field_stats[field]["total"] += 1
                        if value is not None and value != "":
                            field_stats[field]["filled"] += 1
                
                for field, stats in field_stats.items():
                    completion_rate = (stats["filled"] / stats["total"]) * 100 if stats["total"] > 0 else 0
                    stats_data.append({
                        "Field": field,
                        "Total Records": stats["total"],
                        "Filled Records": stats["filled"],
                        "Completion Rate": f"{completion_rate:.1f}%"
                    })
            
            return stats_data
            
        except Exception as e:
            self.logger.error(f"Error creating statistics DataFrame: {str(e)}")
            return [{"Field": "Error", "Total Records": 0, "Filled Records": 0, "Completion Rate": "0%"}]
    
    async def save_template(self, name: str, selectors: Dict[str, str], description: Optional[str] = None):
        """Save scraping template"""
        try:
            template = {
                "name": name,
                "selectors": selectors,
                "description": description or "",
                "created_at": datetime.now().isoformat(),
                "id": str(uuid.uuid4())
            }
            
            file_path = os.path.join(self.templates_dir, f"{name}.json")
            async with aiofiles.open(file_path, 'w', encoding='utf-8') as f:
                await f.write(json.dumps(template, indent=2, ensure_ascii=False))
            
            self.logger.info(f"Template saved: {name}")
            
        except Exception as e:
            self.logger.error(f"Error saving template: {str(e)}")
            raise e
    
    async def get_templates(self) -> List[Dict[str, Any]]:
        """Get all saved templates"""
        try:
            templates = []
            
            if os.path.exists(self.templates_dir):
                for filename in os.listdir(self.templates_dir):
                    if filename.endswith('.json'):
                        file_path = os.path.join(self.templates_dir, filename)
                        async with aiofiles.open(file_path, 'r', encoding='utf-8') as f:
                            content = await f.read()
                            template = json.loads(content)
                            templates.append(template)
            
            return templates
            
        except Exception as e:
            self.logger.error(f"Error getting templates: {str(e)}")
            return []
    
    async def get_template(self, name: str) -> Optional[Dict[str, Any]]:
        """Get specific template by name"""
        try:
            file_path = os.path.join(self.templates_dir, f"{name}.json")
            
            if os.path.exists(file_path):
                async with aiofiles.open(file_path, 'r', encoding='utf-8') as f:
                    content = await f.read()
                    return json.loads(content)
            else:
                return None
                
        except Exception as e:
            self.logger.error(f"Error getting template {name}: {str(e)}")
            return None
    
    async def get_statistics(self) -> Dict[str, Any]:
        """Get processing statistics"""
        try:
            stats = {
                "total_templates": 0,
                "total_exports": 0,
                "last_export": None,
                "data_directory_size": 0,
                "templates_directory_size": 0
            }
            
            # Count templates
            if os.path.exists(self.templates_dir):
                template_files = [f for f in os.listdir(self.templates_dir) if f.endswith('.json')]
                stats["total_templates"] = len(template_files)
            
            # Count exports and get last export
            if os.path.exists(self.data_dir):
                export_files = [f for f in os.listdir(self.data_dir) if f.endswith(('.xlsx', '.json'))]
                stats["total_exports"] = len(export_files)
                
                if export_files:
                    # Get most recent file
                    file_paths = [os.path.join(self.data_dir, f) for f in export_files]
                    most_recent = max(file_paths, key=os.path.getctime)
                    stats["last_export"] = os.path.basename(most_recent)
            
            # Calculate directory sizes
            stats["data_directory_size"] = self._get_directory_size(self.data_dir)
            stats["templates_directory_size"] = self._get_directory_size(self.templates_dir)
            
            return stats
            
        except Exception as e:
            self.logger.error(f"Error getting statistics: {str(e)}")
            return {"error": str(e)}
    
    def _get_directory_size(self, directory: str) -> int:
        """Get directory size in bytes"""
        try:
            total_size = 0
            if os.path.exists(directory):
                for dirpath, dirnames, filenames in os.walk(directory):
                    for filename in filenames:
                        filepath = os.path.join(dirpath, filename)
                        if os.path.exists(filepath):
                            total_size += os.path.getsize(filepath)
            return total_size
        except:
            return 0
    
    async def clean_old_files(self, days_old: int = 30):
        """Clean old export files"""
        try:
            if not os.path.exists(self.data_dir):
                return
            
            current_time = datetime.now().timestamp()
            cutoff_time = current_time - (days_old * 24 * 60 * 60)
            
            cleaned_files = []
            for filename in os.listdir(self.data_dir):
                file_path = os.path.join(self.data_dir, filename)
                if os.path.isfile(file_path):
                    file_time = os.path.getctime(file_path)
                    if file_time < cutoff_time:
                        os.remove(file_path)
                        cleaned_files.append(filename)
            
            self.logger.info(f"Cleaned {len(cleaned_files)} old files")
            return cleaned_files
            
        except Exception as e:
            self.logger.error(f"Error cleaning old files: {str(e)}")
            return []
