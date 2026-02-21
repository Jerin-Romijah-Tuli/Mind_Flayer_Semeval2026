#!/usr/bin/env python3
"""
Official Format Checker for Task B - Generation with Reference Passages
Validates prediction file format before evaluation
"""

import json
import sys
from pathlib import Path

def check_format_taskb(prediction_file: str):
    """
    Validate Task B prediction file format
    
    Required format per task:
    {
      "conversation_id": "...",
      "task_id": "...",
      "Collection": "...",
      "input": [...],
      "contexts": [
        {
          "document_id": "...",
          "text": "...",
          "score": float
        }
      ],
      "predictions": [
        {
          "text": "..."
        }
      ]
    }
    """
    
    print("="*80)
    print("TASK B FORMAT VALIDATION")
    print("="*80)
    
    # Check file exists
    if not Path(prediction_file).exists():
        print(f"❌ ERROR: File not found: {prediction_file}")
        return False
    
    # Check file size
    file_size = Path(prediction_file).stat().st_size
    file_size_mb = file_size / (1024 * 1024)
    print(f"\nFile size: {file_size_mb:.2f} MB")
    
    if file_size > 20 * 1024 * 1024:
        print("❌ ERROR: File exceeds 20 MB limit")
        return False
    else:
        print("✅ File size is within limit")
    
    # Load and validate
    issues = []
    warnings = []
    line_count = 0
    empty_contexts_count = 0
    
    print("\nValidating format...")
    
    try:
        with open(prediction_file, 'r', encoding='utf-8') as f:
            for line_num, line in enumerate(f, 1):
                line_count += 1
                
                try:
                    data = json.loads(line)
                except json.JSONDecodeError as e:
                    issues.append(f"Line {line_num}: Invalid JSON - {e}")
                    continue
                
                # Check required top-level fields
                required_fields = ['conversation_id', 'task_id', 'Collection', 'input', 'contexts', 'predictions']
                for field in required_fields:
                    if field not in data:
                        issues.append(f"Line {line_num}: Missing required field '{field}'")
                
                # Check task_id is not empty
                if 'task_id' in data:
                    if not data['task_id']:
                        issues.append(f"Line {line_num}: 'task_id' is empty")
                
                # Check input is a list
                if 'input' in data:
                    if not isinstance(data['input'], list):
                        issues.append(f"Line {line_num}: 'input' must be a list")
                    elif len(data['input']) == 0:
                        warnings.append(f"Line {line_num}: 'input' is empty")
                
                # Check contexts format
                if 'contexts' in data:
                    contexts = data['contexts']
                    
                    if not isinstance(contexts, list):
                        issues.append(f"Line {line_num}: 'contexts' must be a list")
                    else:
                        if len(contexts) == 0:
                            empty_contexts_count += 1
                        
                        if len(contexts) > 10:
                            warnings.append(f"Line {line_num}: 'contexts' has {len(contexts)} items (max recommended: 10)")
                        
                        # Validate each context
                        for ctx_idx, ctx in enumerate(contexts):
                            if not isinstance(ctx, dict):
                                issues.append(f"Line {line_num}, context {ctx_idx}: Must be a dict")
                                continue
                            
                            # Check required context fields
                            if 'document_id' not in ctx:
                                issues.append(f"Line {line_num}, context {ctx_idx}: Missing 'document_id'")
                            
                            if 'text' not in ctx:
                                issues.append(f"Line {line_num}, context {ctx_idx}: Missing 'text'")
                            
                            if 'score' not in ctx:
                                issues.append(f"Line {line_num}, context {ctx_idx}: Missing 'score'")
                            elif not isinstance(ctx['score'], (int, float)):
                                issues.append(f"Line {line_num}, context {ctx_idx}: 'score' must be numeric")
                
                # Check predictions format
                if 'predictions' in data:
                    predictions = data['predictions']
                    
                    if not isinstance(predictions, list):
                        issues.append(f"Line {line_num}: 'predictions' must be a list")
                    elif len(predictions) == 0:
                        issues.append(f"Line {line_num}: 'predictions' is empty")
                    else:
                        # Check first prediction
                        pred = predictions[0]
                        if not isinstance(pred, dict):
                            issues.append(f"Line {line_num}: prediction must be a dict")
                        elif 'text' not in pred:
                            issues.append(f"Line {line_num}: prediction missing 'text' field")
                        elif not pred['text'] or not pred['text'].strip():
                            issues.append(f"Line {line_num}: prediction 'text' is empty")
    
    except Exception as e:
        print(f"\n❌ ERROR reading file: {e}")
        return False
    
    # Print results
    print(f"\n{'='*80}")
    print("VALIDATION RESULTS")
    print(f"{'='*80}")
    print(f"Total lines checked: {line_count}")
    print(f"Empty contexts: {empty_contexts_count} (OK for unanswerable tasks)")
    
    if warnings:
        print(f"\n⚠️  Found {len(warnings)} warning(s):")
        for warning in warnings[:5]:
            print(f"   {warning}")
        if len(warnings) > 5:
            print(f"   ... and {len(warnings) - 5} more warnings")
    
    if issues:
        print(f"\n❌ Found {len(issues)} issue(s):")
        for issue in issues[:10]:
            print(f"   {issue}")
        if len(issues) > 10:
            print(f"   ... and {len(issues) - 10} more issues")
        print(f"\n❌ FORMAT IS INVALID")
        return False
    else:
        print(f"\n✅ ✅ ✅ FORMAT IS VALID FOR THE EVAL SCRIPT ✅ ✅ ✅")
        return True


if __name__ == "__main__":
    if len(sys.argv) < 2:
        prediction_file = '/kaggle/working/predictions_taskB_FINAL.jsonl'
        print(f"Using default file: {prediction_file}")
    else:
        prediction_file = sys.argv[1]
    
    is_valid = check_format_taskb(prediction_file)
    
    sys.exit(0 if is_valid else 1)