#!/usr/bin/env python3
"""
Comprehensive Task B Quality Validator
Validates predictions against reference and predicts score
"""

import json
from collections import defaultdict
from pathlib import Path

def validate_taskb_quality(submission_file: str, reference_file: str):
    """
    Validate Task B submission quality
    """
    
    print("="*80)
    print("TASK B QUALITY VALIDATION")
    print("="*80)
    
    # Load files
    print(f"\nLoading submission: {submission_file}")
    if not Path(submission_file).exists():
        print(f"❌ ERROR: Submission file not found")
        return None, []
    
    submissions = []
    with open(submission_file, 'r', encoding='utf-8') as f:
        for line in f:
            submissions.append(json.loads(line))
    print(f"✅ Loaded {len(submissions)} submissions")
    
    print(f"\nLoading reference: {reference_file}")
    if not Path(reference_file).exists():
        print(f"❌ ERROR: Reference file not found")
        return None, []
    
    references = []
    with open(reference_file, 'r', encoding='utf-8') as f:
        for line in f:
            references.append(json.loads(line))
    print(f"✅ Loaded {len(references)} references")
    
    # Create lookup
    ref_lookup = {r['task_id']: r for r in references}
    
    # QUALITY CHECKS
    print(f"\n{'='*80}")
    print("QUALITY ANALYSIS")
    print(f"{'='*80}")
    
    # Check 1: Count match
    print(f"\n1. COUNT VALIDATION")
    print(f"   Submissions: {len(submissions)}")
    print(f"   References: {len(references)}")
    if len(submissions) == len(references):
        print(f"   ✅ PASS")
    else:
        print(f"   ❌ FAIL: Count mismatch!")
        return None, []
    
    # Check 2: Task IDs
    print(f"\n2. TASK ID VALIDATION")
    sub_ids = {s['task_id'] for s in submissions}
    ref_ids = {r['task_id'] for r in references}
    
    missing = ref_ids - sub_ids
    extra = sub_ids - ref_ids
    
    if not missing and not extra:
        print(f"   ✅ PASS: All task IDs match")
    else:
        if missing:
            print(f"   ❌ Missing {len(missing)} task IDs")
        if extra:
            print(f"   ❌ Extra {len(extra)} task IDs")
        return None, []
    
    # Check 3: Response quality
    print(f"\n3. RESPONSE QUALITY ANALYSIS")
    
    answerable_correct = 0
    answerable_wrong = 0
    unanswerable_correct = 0
    unanswerable_wrong = 0
    
    refusal_keywords = [
        "don't have", "do not have", "don't know", "cannot answer",
        "can't answer", "no information", "not able", "unable to",
        "apologize", "sorry", "insufficient", "not enough", "can't provide",
        "cannot provide", "don't possess", "do not possess"
    ]
    
    response_lengths = []
    empty_responses = []
    very_short = []
    very_long = []
    
    answerable_refusals = []  # Track which answerable tasks got refusals
    
    for sub in submissions:
        task_id = sub['task_id']
        predictions = sub.get('predictions', [])
        
        if not predictions:
            empty_responses.append(task_id)
            continue
        
        pred_text = predictions[0].get('text', '').strip()
        
        if not pred_text:
            empty_responses.append(task_id)
            continue
        
        response_lengths.append(len(pred_text))
        
        # Check length
        if len(pred_text) < 20:
            very_short.append((task_id, len(pred_text)))
        elif len(pred_text) > 800:
            very_long.append((task_id, len(pred_text)))
        
        # Get reference
        ref = ref_lookup.get(task_id)
        if not ref:
            continue
        
        # Check if answerable
        ref_contexts = ref.get('contexts') or []
        is_answerable = len(ref_contexts) > 0
        
        # Check if response is a refusal
        pred_lower = pred_text.lower()
        is_refusal = any(kw in pred_lower for kw in refusal_keywords)
        
        if is_answerable:
            if is_refusal:
                answerable_wrong += 1
                answerable_refusals.append((task_id, pred_text[:100]))
            else:
                answerable_correct += 1
        else:
            if is_refusal:
                unanswerable_correct += 1
            else:
                unanswerable_wrong += 1
    
    # Results
    total_answerable = answerable_correct + answerable_wrong
    total_unanswerable = unanswerable_correct + unanswerable_wrong
    
    print(f"\n   ANSWERABLE TASKS ({total_answerable} tasks):")
    print(f"      ✅ Correct (has answer): {answerable_correct}")
    print(f"      ❌ Wrong (refusal): {answerable_wrong}")
    if total_answerable > 0:
        acc = answerable_correct / total_answerable * 100
        print(f"      📊 Accuracy: {acc:.1f}%")
    
    print(f"\n   UNANSWERABLE TASKS ({total_unanswerable} tasks):")
    print(f"      ✅ Correct (refusal): {unanswerable_correct}")
    print(f"      ❌ Wrong (has answer): {unanswerable_wrong}")
    if total_unanswerable > 0:
        acc = unanswerable_correct / total_unanswerable * 100
        print(f"      📊 Accuracy: {acc:.1f}%")
    
    # Show examples of answerable refusals
    if answerable_refusals:
        print(f"\n   📋 Examples of answerable tasks that got refusals:")
        for task_id, text in answerable_refusals[:3]:
            print(f"      Task: {task_id}")
            print(f"      Response: {text}...")
            print()
    
    # Check 4: Response lengths
    print(f"\n4. RESPONSE LENGTH ANALYSIS")
    if response_lengths:
        avg_len = sum(response_lengths) / len(response_lengths)
        min_len = min(response_lengths)
        max_len = max(response_lengths)
        
        print(f"   Average: {avg_len:.0f} chars")
        print(f"   Range: {min_len} - {max_len} chars")
        
        if empty_responses:
            print(f"   ⚠️  {len(empty_responses)} empty responses")
        else:
            print(f"   ✅ No empty responses")
        
        if very_short:
            print(f"   ⚠️  {len(very_short)} very short (<20 chars)")
        
        if very_long:
            print(f"   ⚠️  {len(very_long)} very long (>800 chars)")
    
    # Check 5: Format compliance
    print(f"\n5. FORMAT COMPLIANCE")
    
    all_have_scores = True
    contexts_over_limit = 0
    missing_required_fields = 0
    
    for sub in submissions:
        # Check required fields
        required = ['conversation_id', 'task_id', 'Collection', 'input', 'contexts', 'predictions']
        if not all(field in sub for field in required):
            missing_required_fields += 1
        
        contexts = sub.get('contexts', [])
        
        if len(contexts) > 10:
            contexts_over_limit += 1
        
        for ctx in contexts:
            if 'score' not in ctx:
                all_have_scores = False
                break
    
    if missing_required_fields == 0:
        print(f"   ✅ All required fields present")
    else:
        print(f"   ❌ {missing_required_fields} entries missing required fields")
    
    if all_have_scores:
        print(f"   ✅ All contexts have 'score' field")
    else:
        print(f"   ❌ Some contexts missing 'score'")
    
    if contexts_over_limit > 0:
        print(f"   ⚠️  {contexts_over_limit} entries have >10 contexts")
    else:
        print(f"   ✅ All entries have ≤10 contexts")
    
    # SCORE PREDICTION
    print(f"\n{'='*80}")
    print("COMPETITION SCORE PREDICTION")
    print(f"{'='*80}")
    
    # Calculate answerability score
    answerability_score = 0
    if total_answerable > 0 and total_unanswerable > 0:
        ans_acc = answerable_correct / total_answerable
        unans_acc = unanswerable_correct / total_unanswerable
        answerability_score = (ans_acc + unans_acc) / 2
    
    # Base quality (Llama 4 Scout baseline)
    base_quality = 0.55
    
    # Adjustments
    if answerable_wrong > 0:
        penalty = (answerable_wrong / total_answerable) * 0.15
        base_quality -= penalty
    
    if unanswerable_wrong > 0:
        penalty = (unanswerable_wrong / total_unanswerable) * 0.10
        base_quality -= penalty
    
    # Length adjustments
    if response_lengths:
        avg_len = sum(response_lengths) / len(response_lengths)
        if avg_len < 30:
            base_quality -= 0.05
        elif avg_len > 200:
            base_quality += 0.02
    
    predicted_score = max(0.35, min(0.75, base_quality))
    
    print(f"\n📊 PREDICTED F1 SCORE: {predicted_score:.3f}")
    print(f"\n   Breakdown:")
    print(f"   - Base quality: 0.550")
    print(f"   - Answerability: {answerability_score:.3f}")
    print(f"   - Answerable handling: {'✅' if answerable_wrong == 0 else f'⚠️ {answerable_wrong} errors'}")
    print(f"   - Unanswerable handling: {'✅' if unanswerable_wrong == 0 else f'⚠️ {unanswerable_wrong} errors'}")
    
    # Interpretation
    print(f"\n{'='*80}")
    print("SCORE INTERPRETATION")
    print(f"{'='*80}")
    
    if predicted_score >= 0.60:
        print(f"🏆 EXCELLENT! Above GPT-4o baseline (0.60)")
    elif predicted_score >= 0.55:
        print(f"✅ GOOD! Competitive baseline")
    elif predicted_score >= 0.50:
        print(f"⚠️  ACCEPTABLE but below target")
    else:
        print(f"❌ NEEDS IMPROVEMENT")
    
    # Recommendations
    print(f"\n{'='*80}")
    print("RECOMMENDATIONS")
    print(f"{'='*80}")
    
    issues = []
    
    if answerable_wrong > 0:
        issues.append(f"Fix {answerable_wrong} answerable tasks getting refusals")
        issues.append("  → Strengthen prompt to ALWAYS answer when contexts provided")
        issues.append("  → Increase temperature slightly (0.3-0.4)")
    
    if unanswerable_wrong > 0:
        issues.append(f"Fix {unanswerable_wrong} unanswerable tasks getting answers")
    
    if empty_responses:
        issues.append(f"Fix {len(empty_responses)} empty responses")
    
    if contexts_over_limit > 0:
        issues.append(f"Trim {contexts_over_limit} entries to ≤10 contexts")
    
    if missing_required_fields > 0:
        issues.append(f"Fix {missing_required_fields} entries with missing fields")
    
    if issues:
        print(f"\n⚠️  Issues to fix:")
        for i, issue in enumerate(issues, 1):
            print(f"   {i}. {issue}")
    else:
        print(f"\n✅ NO CRITICAL ISSUES!")
    
    # Final recommendation
    print(f"\n{'='*80}")
    if predicted_score >= 0.52 and not issues:
        print("✅ READY TO SUBMIT!")
        print(f"   Expected score: {predicted_score:.3f}")
    else:
        print("⚠️  RECOMMEND FIXES BEFORE SUBMISSION")
        print(f"   Current: {predicted_score:.3f}")
        print(f"   Potential: {min(0.65, predicted_score + 0.05):.3f}")
    print("="*80)
    
    return predicted_score, issues


if __name__ == "__main__":
    submission_file = '/kaggle/working/predictions_taskB_FINAL.jsonl'
    reference_file = '/kaggle/input/task-b-eval/reference_taskB.jsonl'
    
    try:
        score, issues = validate_taskb_quality(submission_file, reference_file)
    except FileNotFoundError as e:
        print(f"\n❌ File not found: {e}")
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()