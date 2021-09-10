import pandas as pd
from model.database import db_execute


def get_click_comment():
    # clicks frame
    sql = "select * from clicks where deletedAt is null"
    re = db_execute(sql)
    cf = pd.DataFrame(re)
    cf['createdAt'] = cf['createdAt'].dt.strftime('%y-%m-%d')
    cf['one'] = 1
    cf = cf.groupby(['userId', 'createdAt', 'diaryId', 'emotionType', 'emotionLevel'])[
        'one'].sum().reset_index()
    cf_emotion = pd.pivot_table(cf, index=['userId', 'createdAt'],
                                columns=['emotionType'], values='emotionLevel')
    cf_diary = pd.pivot_table(cf, index=['userId', 'createdAt'],
                              columns=['diaryId'], values='one')
    cf = pd.merge(cf_emotion, cf_diary, 'left', on=['userId', 'createdAt'])
    # comments frame
    sql = "select * from comments where deletedAt is null"
    result = db_execute(sql)
    dq = pd.DataFrame(result)
    dq['createdAt'] = dq['updatedAt'].dt.strftime('%y-%m-%d')
    dq_emotion = pd.pivot_table(dq, index=['userId', 'createdAt'],
                                columns=['userEmotionType'], values='userEmotionLevel')
    dq_diary = pd.pivot_table(dq, index=['userId', 'createdAt'],
                              columns=['diaryId'], values='emotionLevel')
    dq = pd.merge(dq_emotion, dq_diary, 'left', on=['userId', 'createdAt'])
    da = pd.concat([cf, dq]).fillna(0).sort_index()
    print(da.shape)
    return da


get_click_comment()